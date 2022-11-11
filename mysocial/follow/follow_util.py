import logging

from authors.models.author import Author
from authors.util import AuthorUtil
from follow.models import Follow

logger = logging.getLogger(__name__)


class FollowUtil:
    @staticmethod
    def get_followers(target: Author):
        """
        Get all followers for target Author

        :param target:
        :return:

        Remember to catch errors!
        """
        follower_paths = Follow.objects.values_list('actor', flat=True).filter(target=target.get_url(), has_accepted=True)
        follow_ids = list(map(lambda f: AuthorUtil.from_author_url_to_local_id(f), follower_paths))
        # todo(turnip): support remote author
        return Author.objects.filter(official_id__in=follow_ids)

    @staticmethod
    def are_followers(follower: Author, target: Author):
        """
        Checks if follower Author follows target Author

        :param follower:
        :param target:
        :return:
        """
        try:
            Follow.objects.get(actor=follower, target=target, has_accepted=True)
            return True  # did not return a does not exist error
        except Follow.DoesNotExist:
            return False
        except Exception as e:
            logger.error(f"FollowUtil: are_real_friends: unknown error: {e}")

    @staticmethod
    def get_real_friends(actor: Author):
        """
        Get all real friends

        :param actor:
        :return:

        Remember to catch errors!
        """
        # reference: https://stackoverflow.com/a/9727050/17836168
        # to get real friends, get all my followers (A) and get everyone who follows me (B)
        # then, intersect at A and B, those are real friends
        follower_ids = Follow.objects.values_list('actor', flat=True).filter(target=actor, has_accepted=True)
        following_ids = Follow.objects.values_list('target', flat=True).filter(actor=actor, has_accepted=True)
        # reference: https://stackoverflow.com/a/6369558/17836168
        friend_ids = set(follower_ids).intersection(following_ids)
        return Author.objects.filter(official_id__in=friend_ids)

    @staticmethod
    def are_real_friends(actor: Author, target: Author):
        try:
            Follow.objects.get(actor=actor, target=target, has_accepted=True)
            Follow.objects.get(actor=target, target=actor, has_accepted=True)
            return True  # did not return a does not exist error
        except Follow.DoesNotExist:
            return False
        except Exception as e:
            logger.error(f"FollowUtil: are_real_friends: unknown error: {e}")
