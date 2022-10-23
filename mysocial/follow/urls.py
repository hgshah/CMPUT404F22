from django.urls import path

from . import views
from authors.urls import app_name as authors_app_name

# We have our paths here explicit so it's self-documenting and shows up in the django
# web browser interface when we put the wrong url path
app_name = 'follows'
urlpatterns = [
    path(f'{app_name}/incoming/', views.IncomingRequestView.as_view()),
    path(f'{app_name}/incoming/<int:follow_id>', views.IncomingRequestIndividualView.as_view()),
    path(f'{app_name}/outgoing/', views.OutgoingRequestView.as_view()),
    path(f'{authors_app_name}/<uuid:author_id>/followers', views.FollowersView.as_view()),
]
