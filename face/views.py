from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from .models import Collection, Person, Face


def index(request):
    collection = Collection.objects.first()
    if not collection:
        return render(request, 'face/index.html')

    slug = Collection.objects.first().slug
    return redirect('collection_detail', slug)


def collection_detail(request, slug):
    collection = get_object_or_404(Collection, slug=slug)

    if request.method == 'POST':
        photo_file = request.FILES.get('photo')
        if photo_file:
            identified = collection.search_faces(photo_file, max_faces=3)
        else:
            identified = []
        return render(request, 'face/identified.html', {
            'identified': identified,
        })

    person_list = collection.person_set.all().annotate(Count('face'))
    face_count = Face.objects.all().count()

    return render(request, 'face/collection_detail.html', {
        'collection': collection,
        'person_list': person_list,
        'face_count': face_count,
    })


def person_detail(request, collection_slug, pk):
    person = get_object_or_404(Person, collection__slug=collection_slug, pk=pk)
    return render(request, 'face/person_detail.html', {
        'person': person,
    })


def person_photo(request, pk):
    person = get_object_or_404(Person, pk=pk)
    return redirect(person.photo_url)

