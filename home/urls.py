from django.urls import path

from .views import home, about, community, contact, team, testimonial

urlpatterns = [
    path("", home),
    path("about", about),
    path("community", community),
    path("contact", contact),
    path("team", team),
    path("testimonial", testimonial),
]
