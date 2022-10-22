from django.urls import path

from . import views

app_name = 'friendships'
urlpatterns = [
    path('<str:action>/', views.FriendshipView.as_view()),
]
