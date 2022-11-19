
from django.http.response import HttpResponse, HttpResponseNotFound
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework.decorators import action
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from authors.models.author import Author
from comment.serializers import CommentSerializer, CreateCommentSerializer
from .models import Comment
from post.models import Post
from rest_framework import status
import logging

logger = logging.getLogger("mylogger")
class CommentView(GenericAPIView):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateCommentSerializer
        else:
            return CommentSerializer

    def get_queryset(self):
        return Comment.objects.all()

    @extend_schema(
        summary = "comment_get_comments_for_post",
        responses = inline_serializer(
            name='CommentList',
            fields={
                'type': serializers.CharField(),
                'items': CommentSerializer(many=True)
            }
        ),
        tags=['comment']
    )
    @action(detail=True, methods=['get'], url_name='comment_get')
    def get(self, request: Request, *args, **kwargs) -> HttpResponse:
        try:
            post = Post.objects.get(official_id=kwargs['post_id'])
            comments = Comment.objects.filter(post = post)
            serializer = CommentSerializer(comments, many = True)
            return Response({'type': 'comments', 'items': serializer.data})
        except Exception as e:
            logger.info(e)
            return HttpResponseNotFound

    @extend_schema(
            summary = "comment_create_comment",
            request = CreateCommentSerializer,
            
            responses = CommentSerializer,
            tags=['comment']
        )
    @action(detail=True, methods=['get'], url_name='comment_post')
    def post(self, request: Request, *args, **kwargs) -> HttpResponse:
        """
        User story: As an author, I want to comment on posts that I can access
        """
        try:
            serializer = CreateCommentSerializer(data=request.data)
            if serializer.is_valid():
                data = serializer.data
                data['author'] = Author.objects.get(official_id = self.request.user.official_id)
                data['post'] = Post.objects.get(official_id = kwargs['post_id'])
                comment = serializer.create(validated_data=data)
                return Response(CommentSerializer(comment).data, status = status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return HttpResponseNotFound
