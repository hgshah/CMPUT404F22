from django.urls import path
from . import views

urlpatterns = [
    path('authors/<uuid:author_id>/posts/', views.CreationPostView.as_view()),
]