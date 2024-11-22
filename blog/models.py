from django.db import models
from app.models import AbstractBaseModel, User

# Create your models here.

class Author(AbstractBaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    class Meta:
        db_table = 'blog_author'
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['user_id']),
            models.Index(fields=['updated_at']),
            models.Index(fields=['created_at'])
        ]

    def __str__(self):
        return self.name

class Post(AbstractBaseModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        db_table = 'blog_post'
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

        indexes = [
            models.Index(fields=['published_date']),
            models.Index(fields=['author_id']),
            models.Index(fields=['updated_at']),
            models.Index(fields=['created_at'])
        ]

    def __str__(self):
        return self.title

class Comment(AbstractBaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    body = models.TextField()

    class Meta:
        db_table = 'blog_comment'
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

        indexes = [
            models.Index(fields=['post_id']),
            models.Index(fields=['author_id']),
            models.Index(fields=['updated_at']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.body