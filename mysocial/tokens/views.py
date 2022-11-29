from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from authors.serializers.author_serializer import AuthorSerializer


# from https://stackoverflow.com/q/66264736/17836168
class ObtainCookieAuthToken(ObtainAuthToken):
    """
    Override default ObtainAuthToken view from rest_framework. This is how frontend should log in.
    """

    @extend_schema(
        request=inline_serializer(
            name='Login',
            fields={
                'username': serializers.CharField(),
                'password': serializers.CharField(),
            }
        ),
        responses=inline_serializer(
            name='Token',
            fields={
                'type': serializers.CharField(),
                'token': serializers.CharField(),
                'author': AuthorSerializer()
            }
        ),
    )
    def post(self, request, *args, **kwargs) -> Response:
        """For the login flow, look at this reference:
        https://github.com/hgshah/cmput404-project/blob/staging/endpoints.txt#L145 """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=401)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        serializer = AuthorSerializer(
            user,
            context={
                "host": request.get_host()
            })
        # todo(turnip): document in the endpoints.txt
        return Response({
            'type': 'token',
            'token': str(token),
            'author': serializer.data,
        })
