from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('collections/<slug:slug>/', views.collection_detail, name='collection_detail'),
    path('collections/<slug:collection_slug>/people/<int:pk>/', views.person_detail, name='person_detail'),
    path('person/<int:pk>.jpg', views.person_photo, name='person_photo'),
]

