from django.urls import path, include
from .community import create_community_post, create_comment
from .chatbot import get_chatbot_response, get_chatbot_history
from .chatbot.bedrock import (
    generate_calorie_recommendations,
    get_recommendations_based_on_medical_history,
)


urlpatterns = [
    path("community/create", create_community_post),
    path("community/comment/create", create_comment),
    path("chatbot/get_response", get_chatbot_response),
    path("chatbot/get_history", get_chatbot_history),
    path("food_track/", include("food_track.urls")),
    path("stream-recommendations", generate_calorie_recommendations),
    path("recommendations", get_recommendations_based_on_medical_history),
]
