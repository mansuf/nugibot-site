from django.urls import path
from .views import diet, vegan


urlpatterns = [path("vegan", vegan), path("diet", diet)]
