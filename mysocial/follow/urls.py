from django.urls import path

from . import views

# We have our paths here explicit so it's self-documenting and shows up in the django
# web browser interface when we put the wrong url path
app_name = 'follow'
urlpatterns = [
    path('incoming/', views.IncomingRequestView.as_view()),
    path('outgoing/', views.OutgoingRequestView.as_view()),
]
