from rest_framework.authtoken.models import Token

from authors.models import Author


class ForceLogin:
    @staticmethod
    def force_login(author: Author):
        """
        Returns a properly formatted header with the token to login
        :param author:
        :return: A dictionary containing the proper key-value token header

        Example how to use::

            token_header = ForceLogin.force_login(actor)
            response = self.client.post(
                f'/authors/{target.official_id}/followers/',
                content_type='application/json',
                **token_header
            )

        """
        token, _ = Token.objects.get_or_create(user=author)
        return {"HTTP_AUTHORIZATION": f"Token {token}"}
