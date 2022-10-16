from django.http.response import HttpResponseNotFound
from rest_framework.generics import GenericAPIView


class AuthorView(GenericAPIView):
    # todo(turnip): serializer class

    def get_queryset(self):
        print("Test 1")
        return HttpResponseNotFound()

    def get_object(self):
        print("Test 2")
        return HttpResponseNotFound()

    def get_serializer_class(self):
        return super().get_serializer_class()
