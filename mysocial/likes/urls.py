from django.urls import path
from . import views

urlpatterns = [
  path('authors/<uuid:author_id>/inbox',
    views.InboxView.as_view()), 
  path('authors/<uuid:author_id>/liked', 
    views.LikedView.as_view()),
  path('authors/<uuid:author_id>/posts/<uuid:post_id>/likes', 
    views.PostLikesView.as_view()),
  path('authors/<uuid:author_id>/posts/<uuid:post_id>/comments/<uuid:comment_id>/likes',
    views.CommentLikesView.as_view()),
]