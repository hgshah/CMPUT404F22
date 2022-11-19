from django.urls import path

from . import views

app_name = 'likes'
urlpatterns = [
    path(f'authors/<uuid:author_id>/posts/<uuid:post_id>/{app_name}', views.LikeView.as_view({'get': 'get_authors_liked_on_post'})),
    path(f'authors/<uuid:author_id>/posts/<uuid:post_id>/comments/<uuid:comment_id>/{app_name}', views.LikeView.as_view({'get': 'get_authors_liked_on_comment'})),
]
