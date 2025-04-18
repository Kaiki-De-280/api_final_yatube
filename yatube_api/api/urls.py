from django.urls import path, include
from .views import (PostViewSet, CommentViewSet,
                    GroupViewSet, FollowViewSet)
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'posts\/(?P<post_id>\d+)\/comments', CommentViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'follow', FollowViewSet)
urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
# r'posts\/\d+\/comments'
