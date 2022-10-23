from django.db import models

# Create your models here.
class Likes(models.Model):
    summary = models.CharField(max_length=100)
    type = 'Like'
    author = models.ForeignKey('authors.Author', on_delete = models.CASCADE)
    object = models.ForeignKey('post.Post', on_delete = models.CASCADE)