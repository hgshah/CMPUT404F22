from django.urls import path

from . import views

urlpatterns = [
    path('', views.AuthorView.as_view(), name='index'),
]