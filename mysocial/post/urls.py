from django.urls import path
from . import views

app_name = 'post'
urlpatterns = [
    path('posts/public/', views.PublicPostView.as_view()),
    path('authors/<uuid:author_id>/posts/<uuid:post_id>/', views.PostView.as_view()),
    path('authors/<uuid:author_id>/posts/', views.CreationPostView.as_view()),
    path('authors/<uuid:author_id>/posts/<uuid:post_id>/share', views.SharePostView.as_view()),
]