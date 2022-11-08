from django.urls import path

from . import views

app_name = 'authors'
urlpatterns = [
    path('', views.AuthorView.as_view({'get': 'retrieve_all'})),
    path('<uuid:author_id>/', views.AuthorView.as_view({'get': 'retrieve'})),
    path('remote-node/', views.RemoteNodeView.as_view()),
]
