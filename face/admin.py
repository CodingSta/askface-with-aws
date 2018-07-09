from django.contrib import admin
from .models import Collection, Person, Face


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['collection', 'name']


@admin.register(Face)
class FaceAdmin(admin.ModelAdmin):
    list_display = ['person', 'meta']

