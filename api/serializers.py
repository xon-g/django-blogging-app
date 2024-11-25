from django.contrib.auth.models import Group
from django.urls import reverse
from app.models import User
from blog.models import Post, Author, Comment
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination

from pprint import pprint

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['url', 'id', 'name', 'email']

class PostPagination(PageNumberPagination):
    page_size = 10

class AuthorDetailSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()
    class Meta:
        model = Author
        fields = ['id', 'name', 'email', 'user', 'posts']

    def get_posts(self, obj):
        posts = obj.post_set.all().order_by('-created_at')
        paginator = PostPagination()
        page = paginator.paginate_queryset(posts, self.context['request'])
        serializer = PostSerializer(page, many=True, context=self.context)
        return paginator.get_paginated_response(serializer.data).data

class PostSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='post-detail', lookup_field='pk')
    author = serializers.StringRelatedField()
    class Meta:
        model = Post
        fields = ['url', 'id', 'title', 'content', 'published_date', 'author']

    def get_url(self, obj):
        return reverse('post-detail', kwargs={'pk': obj.pk})

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'published_date', 'author']


class CommentPagination(PageNumberPagination):
    page_size = 10

class PostDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    author = AuthorSerializer()

    def get_comments(self, obj):
        paginator = CommentPagination()
        comments = obj.comment_set.all().order_by('-created_at')
        page = paginator.paginate_queryset(comments, self.context['request'])
        serializer = CommentSerializer(page, many=True, context=self.context)
        return paginator.get_paginated_response(serializer.data).data

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'published_date', 'author', 'comments']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class CommentCreateSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='comment-detail', lookup_field='pk')
    class Meta:
        model = Comment
        fields = ['url', 'post', 'body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['post'].help_text = 'The post that this comment belongs to.'
        self.fields['body'].help_text = 'The content / body of the comment.'

    def create(self, validated_data):
        author = self.context['request'].user.author
        comment = Comment.objects.create(author=author, **validated_data)
        return comment

class CommentDetailSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)
    author = AuthorSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'