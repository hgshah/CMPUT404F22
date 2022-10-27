from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from authors.serializers.author_serializer import AuthorSerializer


# from https://stackoverflow.com/q/66264736/17836168
class ObtainCookieAuthToken(ObtainAuthToken):
    """
    Override default ObtainAuthToken view from rest_framework to set the token into a
    HttpOnly cookie.
    """

    def post(self, request, *args, **kwargs) -> Response:
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
