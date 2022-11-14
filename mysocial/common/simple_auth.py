
class SimpleAuth:
    #k44, October 19, https://stackoverflow.com/questions/12615154/how-to-get-the-currently-logged-in-users-user-id-in-django 
    @staticmethod
    def authorize_user(author_id, request):
        return author_id == request.user.official_id