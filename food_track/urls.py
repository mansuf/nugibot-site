from django.urls import path
from . import views

app_name = "food_track"

urlpatterns = [
    path("list", views.food_track_list, name="food_track_list"),
    path("add", views.food_track_add, name="food_track_add"),
    path("delete", views.food_track_delete, name="food_track_delete"),
    path(
        "calculate_calorie_metrics",
        views.calculate_calorie_metrics,
        name="food_track_calculate_calorie_metrics",
    ),
]
