from django.shortcuts import render
from django.http import HttpResponse
from .models import Likes
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.request import Request

def index(request):
    return HttpResponse("")

class LikedView(GenericAPIView):
    def function():
        return

class PostLikesView(GenericAPIView):
    #
    def function():
        return
