from django.urls import path
from .community import create_community_post, create_comment


urlpatterns = [
    path("community/create", create_community_post),
    path("community/comment/create", create_comment),
]
