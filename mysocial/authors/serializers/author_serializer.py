from rest_framework import serializers
from authors.models import Author


class AuthorSerializer(serializers.ModelSerializer):
    """
    based on https://stackoverflow.com/a/18426235/17836168
    Note: We can generalize this btw to use in every serializer out there!
    """
    type = serializers.SerializerMethodField('get_type')
    id = serializers.SerializerMethodField('get_id')
    displayName = serializers.CharField(source='display_name')
    profileImage = serializers.CharField(source='profile_image')
    url = serializers.SerializerMethodField('get_url')

    def get_type(self, model: Author):
        return model.get_serializer_field_name()

    def get_url(self, model: Author):
        # they're the same as id, for now
        return self.get_id(model)

    def get_id(self, model: Author):
        # the path after host may vary, e.g. authors/ vs authors/id
        return f"http://{model.host}/{Author.URL_PATH}/{model.official_id}"

    class Meta:
        model = Author
        fields = ('type', 'id', 'url', 'host', 'displayName', 'github', 'profileImage')
