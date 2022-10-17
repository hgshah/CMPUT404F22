from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseNotFound
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from authors.models import Author
from authors.serializers.author_serializer import AuthorSerializer


class AuthorView(GenericAPIView):
    def get_queryset(self):
        return None

    def get(self, request: HttpRequest, author_id: str = None) -> HttpResponse:
        # todo(turnip): pagination
        # todo(turnip): single author
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        # todo(turnip): there might be a better way doing this that can make it surface in the auto docs via serializer
        return Response({
            'type': 'authors',
            'items': serializer.data
        })
        # formatted_list = []
        # for el in Author.objects.all():
        #     formatted_list.append(el.as_json())
        # data = {"data": formatted_list}
        # return Response(status=200, data=data)
