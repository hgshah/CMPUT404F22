from rest_framework import serializers

from authors.models import Author


class AuthorSerializer(serializers.ModelSerializer):
    """
    based on https://stackoverflow.com/a/18426235/17836168
    Note: We can generalize this btw to use in every serializer out there!
    """
    type = serializers.SerializerMethodField('get_type')
    displayName = serializers.CharField(source='display_name')

    def get_type(self, model):
        return model.get_serializer_field_name()

    class Meta:
        model = Author
        # todo(turnip): url, host, profile image
        fields = ('type', 'id', 'username', 'displayName', 'github')
