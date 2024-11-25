from django.urls import include, path
from rest_framework import routers
from .views import UserViewSet, GroupViewSet, AuthorViewSet, PostViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]
