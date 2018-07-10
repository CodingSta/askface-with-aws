import boto3
from collections import OrderedDict
from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from django.shortcuts import resolve_url
from django.utils.functional import cached_property
from jsonfield import JSONField


client = boto3.client('rekognition',
    region_name=settings.AWS_DEFAULT_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)


class Collection(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(validators=[RegexValidator(r'^[a-zA-Z0-9_\.-]+$')])

    def __str__(self):
        return self.name

    def search_faces(self, source_img, max_faces=3):
        response = client.search_faces_by_image(
              CollectionId=self.slug,
              Image={'Bytes': source_img.read()},
              MaxFaces=max_faces)

        identified = OrderedDict()
        for match in response['FaceMatches']:
            similarity = match['Similarity']
            person_pk = int(match['Face']['ExternalImageId'])

            try:
                person = Person.objects.get(pk=person_pk)
            except Person.DoesNotExist:
                pass
            else:
                recent_similarity = identified.get(person, 0)
                identified[person] = max(recent_similarity, similarity)

        return identified

    @classmethod
    def on_post_save(cls, sender, **kwargs):
        if kwargs['created']:
            self = kwargs['instance']
            client.create_collection(CollectionId=self.slug)

    @classmethod
    def on_post_delete(cls, sender, **kwargs):
        self = kwargs['instance']
        client.delete_collection(CollectionId=self.slug)

post_save.connect(Collection.on_post_save, sender=Collection)
post_delete.connect(Collection.on_post_delete, sender=Collection)


class Person(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    @property
    def photo_url(self):
        return self.face_set.first().photo.url

    def get_absolute_url(self):
        return resolve_url('person_detail', self.collection.slug, self.pk)


class Face(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    photo = models.ImageField()
    meta = JSONField()

    @cached_property
    def collection_id(self):
        return self.person.collection.slug

    @cached_property
    def idol_id(self):
        return str(self.person.pk)

    @cached_property
    def face_id(self):
        if self.meta:
            try:
                return self.meta['FaceRecords'][0]['Face']['FaceId']
            except (IndexError, KeyError):
                pass

    @cached_property
    def face_model_version(self):
        if self.meta:
            return self.meta['FaceModelVersion']

    def indexing(self, attributes='ALL'):
        return client.index_faces(
            CollectionId=self.collection_id,
            ExternalImageId=self.idol_id,
            Image={'Bytes': self.photo.read()},
            DetectionAttributes=[attributes])

    @classmethod
    def on_pre_save(cls, sender, **kwargs):
        self = kwargs['instance']

        if not self.meta:
            self.meta = self.indexing()

    @classmethod
    def on_post_delete(cls, sender, **kwargs):
        self = kwargs['instance']
        print('delete face ', self.face_id)
        client.delete_faces(CollectionId=self.collection_id, FaceIds=[self.face_id])

pre_save.connect(Face.on_pre_save, sender=Face)
post_delete.connect(Face.on_post_delete, sender=Face)

