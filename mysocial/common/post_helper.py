from authors.models.author import Author
from mysocial.settings import base
from comment.models import Comment
from comment.serializers import CommentSerializer
from post.serializer import PostSerializer

class PostHelper():
    def add_comments_and_count(author: Author, post):
        try:
            if author:
                node_config = base.REMOTE_CONFIG.get(author.host)
            else:
                node_config = None

            if node_config:
                print("im in here")
                path = f'{post.get_url()}/comments'
                
                response = node_config.get_comments_for_post(path)

                if response.status_code < 200 or response.status_code > 300:
                    return 0, []
                
                return len(response.content), response.content
            else:
                comments = Comment.objects.filter(post = post)
                comment_serializer = CommentSerializer(comments, many = True)
                post = PostSerializer(post).data
                post['commentSrc'] = comment_serializer.data
                post['count'] = len(comments)
                
                return post

        except Exception as e:
            print(e)

