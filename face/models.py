from django.core.validators import RegexValidator
from django.db import models
from jsonfield import JSONField


class Collection(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(validators=[RegexValidator(r'^[a-zA-Z0-9_\.-]+$')])

    def __str__(self):
        return self.name


class Person(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Face(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    photo = models.ImageField()
    meta = JSONField()

