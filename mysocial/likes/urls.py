from django.urls import path
from . import views

urlpatterns = [
  path('authors/<uuid:author_id>/liked'),
  path('authors/<uuid:author_id>/posts/<uuid:post_id>/likes'),
]