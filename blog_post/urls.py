from django.urls import path
from rest_framework import routers

from .views import (
    PostViewSet,
)

app_name = "blog_post"

router = routers.DefaultRouter()
router.register("api/posts", PostViewSet, basename="posts")

urlpatterns = []
urlpatterns += router.urls
