import logging
import types

from django.http.response import HttpResponse, HttpResponseNotFound
from rest_framework.request import Request

from authors.models.author import Author
from authors.util import AuthorUtil
from follow.models import Follow
from mysocial.settings import base
from remote_nodes.node_config_base import NodeConfigBase

logger = logging.getLogger(__name__)


class FollowUtil:
    @staticmethod
    def get_followers(target: Author):
        """
        Get all followers for target Author. Be careful because this gets both remote Author and local Author. Check
        if it's a local author by using author.is_local()

        :param target:
        :return: List of Authors

        Remember to catch errors!
        """
        # todo: support remote authors!
        if target.is_local():
            follower_url_list = Follow.objects.values_list('actor', flat=True).filter(target=target.get_url(),
                                                                                      has_accepted=True)
        else:
            node_config: NodeConfigBase = base.REMOTE_CONFIG.get(target.host)
            if node_config is None:
                print(f"FollowUtil: get_followers: missing NodeConfig: {target.host}")
                return []
            follower_list = node_config.get_all_followers(target)
            follower_url_list = []
            for follow_object in follower_list:
                follow_object: Follow = follow_object # type hinting for IDE
                follower_url_list.append(follow_object.actor)

        # todo: we could optimize this (later) by saving a list of local urls and doing a single database query for
        #  local authors; this implementation gets the local authors one-by-one; alternative will need another list
        #  for local authors, identify which ones are local based on the url, then do an is_in query in Author.objects
        #  doing it like this to make it readable for now
        author_list = []
        for author_url in follower_url_list:
            author, err = AuthorUtil.from_author_url_to_author(author_url)
            if err is None:
                author_list.append(author)
            else:
                print(f"get_followers: Failed getting author from url {author_url} with error: {err}")

        return author_list

    @classmethod
    def get_follow_object(cls, request: Request, target_id: str, follower_id: str) -> (Follow, HttpResponse):
        """Helper function to getting a follow regardless of local or remote"""
        try:
            target = Author.get_author(official_id=target_id)
        except Follow.DoesNotExist:
            return None, HttpResponseNotFound("User not exist on our end")
        except Exception as e:
            print(f"{cls}: {e}")
            return None, HttpResponseNotFound("User not exist on our end")

        try:
            follower = Author.get_author(official_id=follower_id)
        except Follow.DoesNotExist:
            return None, HttpResponseNotFound(
                "The given follower does not seem to exist as a user in any connected nodes")
        except Exception as e:
            print(f"{cls}: {e}")
            return None, HttpResponseNotFound("The given follower does not seem to exist as a user")

        if target.is_local():
            # trust our data
            try:
                follow = Follow.objects.get(target=target.get_url(), actor=follower.get_url())

                if follow.get_author_target() != request.user and not follow.has_accepted:
                    return None, HttpResponseNotFound("User does not follow the following author on our end")

                return follow, None
            except Follow.DoesNotExist:
                return None, HttpResponseNotFound("User does not follow the following author on our end")
            except Exception as e:
                print(f"{cls}: {e}")
                return None, HttpResponseNotFound("User does not follow the following author on our end")
        else:
            # trust THEIR data
            node_config: NodeConfigBase = base.REMOTE_CONFIG.get(target.host)
            if node_config is None:
                print(f"{cls}: get: unknown host: {target.host}")
                return None, HttpResponseNotFound()

            follow = node_config.get_remote_follow(target, follower)
            if follow is None:
                return None, HttpResponseNotFound("User does not follow the following author on our end")

            return follow, None

    @staticmethod
    def are_followers(follower: Author, target: Author) -> bool:
        """
        Checks if follower Author follows target Author

        :param follower:
        :param target:
        :return:
        """
        fake_request = types.SimpleNamespace()
        fake_request.user = target
        follow, err = FollowUtil.get_follow_object(request=fake_request, target_id=target.get_id(), follower_id=follower.get_id())
        if err is not None:
            return False
        return follow.has_accepted

    @staticmethod
    def get_real_friends(target: Author):
        """
        Get all real friends or mutual followers for target Author. Be careful because this gets both remote Author and
        local Author. Check if it's a local author by using author.is_local()

        :param target:
        :return: List of Authors

        Remember to catch errors!
        """
        follower_list = Follow.objects.filter(target=target.get_url(), has_accepted=True)
        friends = []
        for follower_follow_object in follower_list:
            follower = follower_follow_object.get_author_actor()
            if FollowUtil.are_followers(target, follower):
                friends.append(follower)
        return friends

    @staticmethod
    def are_real_friends(actor: Author, target: Author) -> bool:
        return FollowUtil.are_followers(actor, target) and FollowUtil.are_followers(target, actor)
    
    @staticmethod
    def get_following_authors(actor: Author):
        following_ids = Follow.objects.values_list('target', flat=True).filter(actor=actor.get_url(), has_accepted=True)

        author_list = []
        for author_url in following_ids:
            author, err = AuthorUtil.from_author_url_to_author(author_url)
            if err is None:
                author_list.append(author)
            else:
                print(f"get_followers: Failed getting author from url {author_url} with error: {err}")

        return author_list

