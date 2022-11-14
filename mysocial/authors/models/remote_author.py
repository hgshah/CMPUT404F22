from authors.models.author import Author


class RemoteAuthor(Author):
    def save(self, *args, **kwargs):
        raise Exception("Do not save a remote author!!!!")
