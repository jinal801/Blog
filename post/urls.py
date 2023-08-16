
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from post.api import PostViewSet, LikeViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'likes', LikeViewSet)

urlpatterns = [

]
