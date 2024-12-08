from django.urls import path

from .views import (
    home,
    about,
    community,
    contact,
    team,
    testimonial,
    article,
    article2,
    article3,
    chart,
    chatbot,
    diet,
    history,
    calculator,
    track,
    vegan,
)

urlpatterns = [
    path("", home),
    path("about", about),
    path("community", community),
    path("contact", contact),
    path("team", team),
    path("testimonial", testimonial),
    path("article", article),
    path("article2", article2),
    path("article3", article3),
    path("chart", chart),
    path("chatbot", chatbot),
    path("diet", diet),
    path("history", history),
    path("calculator", calculator),
    path("track", track),
    path("vegan", vegan),
]
