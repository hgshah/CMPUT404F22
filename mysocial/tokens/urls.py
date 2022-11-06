from django.urls import path

from . import views

app_name = 'tokens'
urlpatterns = [
    path(f'{app_name}/', views.ObtainCookieAuthToken.as_view()),
]
