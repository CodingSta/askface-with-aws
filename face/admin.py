from django.contrib import admin
from django.db.models import Count
from .models import Collection, Person, Face
from .forms import FaceForm


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'slug']


class FaceInline(admin.TabularInline):
    model = Face
    form = FaceForm


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['pk', 'collection', 'name', 'face_count']
    list_display_links = ['name']
    inlines = [FaceInline]

    def get_queryset(self, request):
        return Person.objects.all().annotate(Count('face'))

    def face_count(self, person):
        return person.face__count

