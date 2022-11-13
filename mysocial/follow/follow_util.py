import logging

from rest_framework.exceptions import ValidationError

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
        :return: List of Authors

        Remember to catch errors!
        """
        follower_url_list = Follow.objects.values_list('actor', flat=True).filter(target=target.get_url(),
                                                                                  has_accepted=True)

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
