import uuid

from django.db import models
from django.db.models import Q

from authors.models.author import Author
from authors.util import AuthorUtil
from common.base_util import BaseUtil
from mysocial.settings import base
from remote_nodes.remote_util import RemoteUtil


class Follow(models.Model):
    """
    actor follows target

    A Follow object is authoritative if:
    1. It's local author following a local author
    2. It's a remote author following a local author

    A Follow object is a reference only if:
    1. It's a local author following a remote author
    """
    FIELD_NAME_HAS_ACCEPTED = 'hasAccepted'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    """url for the actor's author resource NOT the author id and NOT the Author object"""
    actor = models.URLField(validators=[AuthorUtil.validate_author_url], max_length=1000)
    """url for the target's author resource NOT the author id and NOT the Author object"""
    target = models.URLField(validators=[AuthorUtil.validate_author_url], max_length=1000)
    has_accepted = models.BooleanField(default=False)

    """
    remote_url is the url pointing to a related and more authoritative Follow object
    If this is not empty, the other Follow object is our source of truth
    If this is empty, this is the source of truth and you may disregard the other object
    """
    remote_url = models.URLField(blank=True, max_length=1000)
    """
    remote_id is the id of the authoritative Follow object in the other server
    """
    remote_id = models.UUIDField(default=uuid.uuid4, editable=False)

    def __init__(self, *args, **kwargs):
        self._author_actor: Author = None
        self._author_target: Author = None
        super().__init__(*args, **kwargs)

    class Meta:
        unique_together = (('actor', 'target'),)
        get_latest_by = 'id'

    def get_author_actor(self) -> Author:
        """Get the author object for the given actor in actor url"""
        if self._author_actor is None:
            self._author_actor, err = AuthorUtil.from_author_url_to_author(self.actor)
            if err is not None:
                raise err
        return self._author_actor

    def get_author_target(self) -> Author:
        """Get the author object for the given target in target url"""
        if self._author_target is None:
            self._author_target, err = AuthorUtil.from_author_url_to_author(self.target)
            if err is not None:
                raise err
        return self._author_target

    def get_local_url(self):
        """
        Returns the url to get this Follow object
        """
        return f"{self.target}/followers/{self.get_author_actor().get_id()}"

    def get_url(self):
        if bool(self.remote_url):
            return self.remote_url
        return self.get_local_url()

    @staticmethod
    def get_serializer_field_name():
        return "Follow"

    def __str__(self):
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
