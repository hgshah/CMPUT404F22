from django.urls import path

from . import views

app_name = 'authors'
urlpatterns = [
    path(f'{app_name}/', views.AuthorView.as_view({'get': 'retrieve_all'})),
    path(f'{app_name}/self/', views.AuthorSelfView.as_view()),
    path(f'{app_name}/<uuid:author_id>/', views.AuthorView.as_view({'get': 'retrieve'})),
    path('remote-node/', views.RemoteNodeView.as_view()),
]
