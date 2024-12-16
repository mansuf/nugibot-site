from django.urls import path
from .community import create_community_post, create_comment
from .chatbot import get_chatbot_response


urlpatterns = [
    path("community/create", create_community_post),
    path("community/comment/create", create_comment),
    path("chatbot/get_response", get_chatbot_response)
]
