from django.db import models

# Create your models here.
from django.utils import timezone


class FoodTrack(models.Model):
    FOOD_TYPES = (
        ("Breakfast", "Breakfast"),
        ("Lunch", "Lunch"),
        ("Dinner", "Dinner"),
        ("Dessert", "Dessert"),
    )

    food_type = models.CharField(max_length=20, choices=FOOD_TYPES)
    food_name = models.CharField(max_length=100)
    calorie = models.IntegerField()
    sugar = models.FloatField()
    fiber = models.FloatField()
    protein = models.FloatField()
    time = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-time"]

    def __str__(self):
        return f"{self.food_name} - {self.food_type}"

    def to_dict(self):
        return {
            "id": self.id,
            "foodType": self.food_type,
            "foodName": self.food_name,
            "calorie": self.calorie,
            "sugar": self.sugar,
            "fiber": self.fiber,
            "protein": self.protein,
            "time": self.time.strftime("%d %B %Y %H:%M"),
        }
