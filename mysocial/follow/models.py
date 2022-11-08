from django.db import models

from authors.models.author import validate_author_url
from mysocial import settings


class Follow(models.Model):
    """
    todo(turnip): WIP
    actor follows target
    """
    FIELD_NAME_HAS_ACCEPTED = 'hasAccepted'

    actor = models.URLField(settings.base.AUTH_USER_MODEL, validators=[validate_author_url])
    target = models.URLField(settings.base.AUTH_USER_MODEL, validators=[validate_author_url])
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
