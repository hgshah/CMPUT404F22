from django.urls import path
from . import views

urlpatterns = [
    path('posts/public/', views.PublicPostView.as_view()),
    path('authors/<uuid:author_id>/posts/', views.CreationPostView.as_view()),
]