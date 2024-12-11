from django.urls import path
from .community import create_community_post


urlpatterns = [path("community/create", create_community_post)]
