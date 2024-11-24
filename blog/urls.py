from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/load-more-comments/', views.LoadMoreCommentsView.as_view(), name='post_load_more_comments'),
    path('posts/<int:pk>/comment/', views.CommentCreateView.as_view(), name='comment_create'),
]

author_urlpatterns = [
    path('authors/', views.AuthorListView.as_view(), name='author_list'),
    path('authors/<int:pk>', views.AuthorDetailView.as_view(), name='author_detail'),
]

urlpatterns += author_urlpatterns