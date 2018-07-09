import boto3
from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
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

'''
    @classmethod
    def on_post_delete(cls, sender, **kwargs):
        self = kwargs['instance']
        face_id_list = [face.face_id for face in self.face_set.all()]
        print('delete face_id_list', face_id_list)
        client.delete_faces(CollectionId=self.collection_id, FaceIds=face_id_list)

post_delete.connect(Person.on_post_delete, sender=Person)
'''


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

    @classmethod
    def on_pre_save(cls, sender, **kwargs):
        self = kwargs['instance']

        if not self.meta:
            self.meta = client.index_faces(
                CollectionId=self.collection_id,
                ExternalImageId=self.idol_id,
                Image={'Bytes': self.photo.read()},
                DetectionAttributes=['ALL'])

    @classmethod
    def on_post_delete(cls, sender, **kwargs):
        self = kwargs['instance']
        print('delete face ', self.face_id)
        client.delete_faces(CollectionId=self.collection_id, FaceIds=[self.face_id])

pre_save.connect(Face.on_pre_save, sender=Face)
post_delete.connect(Face.on_post_delete, sender=Face)

