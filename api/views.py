from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import Group
from app.models import User
from blog.models import Post, Comment, Author

from rest_framework import permissions, viewsets, generics
from rest_framework.filters import SearchFilter, OrderingFilter

from .serializers \
import UserSerializer, \
    GroupSerializer, \
    AuthorSerializer, \
    AuthorDetailSerializer, \
    PostSerializer, \
    PostDetailSerializer, \
    PostCreateSerializer, \
    CommentSerializer, \
    CommentCreateSerializer, \
    CommentDetailSerializer

from pprint import pprint

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class AuthorViewSet(viewsets.ModelViewSet):
    """
    API endpoint to list or retrieve authors
    """
    queryset = Author.objects.all().order_by('-created_at')

    def get_serializer_class(self):
        if self.action == 'list':
            return AuthorSerializer
        elif self.action == 'retrieve':
            return AuthorDetailSerializer
        return self.serializer_class

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint to list or retrieve posts
    """
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer

    def get_serializer_class(self):
        pprint("Action: " + self.action)
        if self.action == 'list':
            return PostSerializer
        elif self.action == 'create':
            return PostCreateSerializer
        elif self.action == 'retrieve':
            return PostDetailSerializer
        return self.serializer_class

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint to list or retrieve comments
    """
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentDetailSerializer

    def get_serializer_class(self):
        pprint("Action: " + self.action)
        if self.action == 'list':
            return CommentSerializer
        elif self.action == 'create':
            return CommentCreateSerializer
        elif self.action == 'retrieve':
            return CommentDetailSerializer
        return self.serializer_class

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context