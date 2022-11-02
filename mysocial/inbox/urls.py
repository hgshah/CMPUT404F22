from django.urls import path
from . import views

urlpatterns = [
  path('authors/<uuid:author_id>/inbox', views.InboxView.as_view()),
]
