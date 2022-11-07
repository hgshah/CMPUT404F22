from django.db import models

from authors.models.author import validate_author_url
from mysocial import settings


class Follow(models.Model):
    """
    actor follows target
    """
    FIELD_NAME_HAS_ACCEPTED = 'hasAccepted'

    # todo(turnip): change to url
    actor = models.URLField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, validators=[validate_author_url])
    target = models.URLField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, validators=[validate_author_url])
    has_accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = (('actor', 'target'),)
        get_latest_by = 'id'

    @staticmethod
    def get_serializer_field_name():
        return "Follow"

    def __str__(self):
        status = 'follows' if self.has_accepted else 'wants to follow'
        return f'{self.actor} {status} {self.target}'
