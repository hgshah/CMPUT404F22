from django.db import models

from authors.util import AuthorUtil


class Follow(models.Model):
    """
    todo(turnip): WIP
    actor follows target
    """
    FIELD_NAME_HAS_ACCEPTED = 'hasAccepted'

    actor = models.URLField(validators=[AuthorUtil.validate_author_url])
    target = models.URLField(validators=[AuthorUtil.validate_author_url])
    has_accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = (('actor', 'target'),)
        get_latest_by = 'id'

    @staticmethod
    def get_serializer_field_name():
        return "Follow"

    def __str__(self):
        # todo(turnip): make calls to server
        actor, _ = AuthorUtil.from_author_url_to_author(self.actor)
        actor_name = ""
        if actor is not None:
            actor_name = str(actor)
        target, _ = AuthorUtil.from_author_url_to_author(self.target)
        target_name = ""
        if target is not None:
            target_name = str(target)
        status = 'follows' if self.has_accepted else 'wants to follow'
        return f'{actor_name} {status} {target_name}'
