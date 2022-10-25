from django.db import models
from django.contrib.postgres.fields import ArrayField

'''
example like object:
 {
     "@context": "https://www.w3.org/ns/activitystreams",
     "summary": "Lara Croft Likes your post",         
     "type": "Like",
     "author":{
         "type":"author",
         "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
         "host":"http://127.0.0.1:5454/",
         "displayName":"Lara Croft",
         "url":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
         "github":"http://github.com/laracroft",
         "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
     },
     "object":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e"
}
'''
# Create your models here.
class Like(models.Model):
    context = models.CharField(max_length=400)
    summary = models.CharField(max_length=400)
    type = 'like'  # requirements spelled with capital l
    author = models.ForeignKey('authors.Author', on_delete = models.CASCADE)
    object = models.CharField(max_length=400)

# class Liked(models.Model):
#     type = 'liked'
#     items = ArrayField(models.ForeignKey('likes.Likes', on_delete = models.CASCADE), null = True, blank = True)