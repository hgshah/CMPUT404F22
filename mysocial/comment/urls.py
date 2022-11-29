from django.urls import path
from . import views

app_name = 'comment'
urlpatterns = [
    path('authors/<uuid:author_id>/posts/<uuid:post_id>/comments', views.CommentView.as_view()),
]