from django.http.response import HttpResponse, HttpResponseNotFound
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.request import Request

from authors.models import Author
from authors.serializers.author_serializer import AuthorSerializer
from common import PaginationHelper


class AuthorView(GenericAPIView):
    def get_queryset(self):
        return Author.objects.all()

    @staticmethod
    def _get_all_authors(request: Request) -> HttpResponse:
        # lazy query set serialization so it's fine if this goes first
        authors = Author.objects.all()
        serializer = AuthorSerializer(
            authors,
            many=True,
            context={
                "host": request.get_host()
            })
        data = serializer.data

        data, err = PaginationHelper.paginate_serialized_data(request, data)

        if err is not None:
            print("AuthorView: _get_all_authors:", err)
            return HttpResponseNotFound()

        return Response({
            'type': 'authors',
            'items': data
        })

    @staticmethod
    def _get_author(request: Request, author_id: str) -> HttpResponse:
        try:
            author = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return HttpResponseNotFound()
        serializer = AuthorSerializer(
            author,
            context={
                "host": request.get_host()
            })
        return Response(serializer.data)

    def get(self, request: Request, author_id: str = None) -> HttpResponse:
        if author_id is None:
            return self._get_all_authors(request)
        else:
            return self._get_author(request, author_id)
