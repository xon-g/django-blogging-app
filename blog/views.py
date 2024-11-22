from ninja import NinjaAPI
from .models import Post, Comment
from ninja import Schema


class PostSchema(Schema):
    id: int
    title: str
    author: str
    published_date: str

class CommentSchema(Schema):
    id: int
    text: str

api = NinjaAPI()

class PostList(NinjaAPI):
    @api.get("/posts/")
    def list(self, request):
        posts = Post.objects.filter(published=True)
        return [{"id": post.id, "title": post.title, "author": post.author, "published_date": post.published_date} for post in posts]

class PostDetail(NinjaAPI):
    @api.get("/posts/{post_id}/")
    def detail(self, request, post_id: int):
        post = Post.objects.get(id=post_id)
        comments = post.comments.all()
        return {"post": {"id": post.id, "title": post.title, "author": post.author, "published_date": post.published_date}, "comments": [{"id": comment.id, "text": comment.text} for comment in comments]}

class CommentCreate(NinjaAPI):
    @api.post("/posts/{post_id}/comment/")
    def create(self, request, post_id: int, text: str):
        post = Post.objects.get(id=post_id)
        comment = Comment(post=post, text=text)
        comment.save()
        return {"id": comment.id, "text": comment.text}