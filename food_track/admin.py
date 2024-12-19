from django.contrib import admin
from .models import FoodTrack


@admin.register(FoodTrack)
class FoodTrackAdmin(admin.ModelAdmin):
    list_display = (
        "food_name",
        "food_type",
        "calorie",
        "sugar",
        "fiber",
        "protein",
        "time",
    )
    list_filter = ("food_type", "time")
    search_fields = ("food_name", "food_type")
    ordering = ("-time",)
