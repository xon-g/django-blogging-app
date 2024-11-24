from django.urls import path
from . import views

# Authentication routes
urlpatterns = [
    path('user/login/', views.UserLoginView.as_view(), name='user_login'),
    path('user/logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('user/register/', views.UserRegisterView.as_view(), name='user_register'),
]

posts_urlpatterns = [
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/load-more-comments/', views.LoadMoreCommentsView.as_view(), name='post_load_more_comments'),
    path('posts/<int:pk>/comment/', views.CommentCreateView.as_view(), name='comment_create'),
]

author_urlpatterns = [
    path('authors/', views.AuthorListView.as_view(), name='author_list'),
    path('authors/<int:pk>', views.AuthorDetailView.as_view(), name='author_detail'),
    path('authors/<int:pk>/load-more-posts/', views.LoadMorePostsView.as_view(), name='author_load_more_posts'),
]

urlpatterns += author_urlpatterns + posts_urlpatterns