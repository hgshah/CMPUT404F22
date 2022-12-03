import logging

from rest_framework.exceptions import ValidationError

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

    @staticmethod
    def are_followers(follower: Author, target: Author) -> bool:
        """
        Checks if follower Author follows target Author

        :param follower:
        :param target:
        :return:
        """
        try:
            Follow.objects.get(actor=follower.get_url(), target=target.get_url(), has_accepted=True)
            return True  # did not return a does not exist error
        except Follow.DoesNotExist:
            return False
        except Exception as e:
            logger.error(f"FollowUtil: are_real_friends: unknown error: {e}")

    @staticmethod
    def get_real_friends(actor: Author):
        """
        Get all real friends or mutual followers for target Author. Be careful because this gets both remote Author and
        local Author. Check if it's a local author by using author.is_local()

        :param actor:
        :return: List of Authors

        Remember to catch errors!
        """
        # reference: https://stackoverflow.com/a/9727050/17836168
        # to get real friends, get all my followers (A) and get everyone who follows me (B)
        # then, intersect at A and B, those are real friends
        follower_ids = Follow.objects.values_list('actor', flat=True).filter(target=actor.get_url(), has_accepted=True)
        following_ids = Follow.objects.values_list('target', flat=True).filter(actor=actor.get_url(), has_accepted=True)
        # reference: https://stackoverflow.com/a/6369558/17836168
        friend_ids = set(follower_ids).intersection(following_ids)

        author_list = []
        for author_url in friend_ids:
            author, err = AuthorUtil.from_author_url_to_author(author_url)
            if err is None:
                author_list.append(author)
            else:
                print(f"get_followers: Failed getting author from url {author_url} with error: {err}")

        return author_list

    @staticmethod
    def are_real_friends(actor: Author, target: Author) -> bool:
        try:
            Follow.objects.get(actor=actor.get_url(), target=target.get_url(), has_accepted=True)
            Follow.objects.get(actor=target.get_url(), target=actor.get_url(), has_accepted=True)
            return True  # did not return a does not exist error
        except Follow.DoesNotExist:
            return False
        except Exception as e:
            logger.error(f"FollowUtil: are_real_friends: unknown error: {e}")
    
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

