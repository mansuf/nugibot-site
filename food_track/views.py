import json
from django.http import JsonResponse
from django.db.models import Q
from django.db.models import Sum
from django.utils import timezone
import calendar

from .models import FoodTrack


def food_track_list(request):
    search_query = request.GET.get("search", "")

    if search_query:
        foods = FoodTrack.objects.filter(
            Q(food_name__icontains=search_query) | Q(food_type__icontains=search_query)
        )
    else:
        foods = FoodTrack.objects.all()

    data = [food.to_dict() for food in foods]
    return JsonResponse(data, safe=False)


def food_track_add(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            food = FoodTrack.objects.create(
                food_type=data["foodType"],
                food_name=data["foodName"],
                calorie=data["calorie"],
                sugar=data["sugar"],
                fiber=data["fiber"],
                protein=data["protein"],
            )
            return JsonResponse(food.to_dict(), status=201)
        except (json.JSONDecodeError, KeyError) as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Only POST method is allowed"}, status=405)


def food_track_delete(request):
    if request.method == "DELETE":
        try:
            data = json.loads(request.body)
            food_id = data.get("id")
            try:
                food = FoodTrack.objects.get(id=food_id)
                food.delete()
                return JsonResponse({"message": "Deleted successfully"}, status=204)
            except FoodTrack.DoesNotExist:
                return JsonResponse({"error": "Food not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Only DELETE method is allowed"}, status=405)


def calculate_calorie_metrics(request, raw=False):
    # Get current date and time
    now = timezone.now()

    # Calculate start and end of current month
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_day = calendar.monthrange(now.year, now.month)[1]
    end_of_month = now.replace(
        day=last_day, hour=23, minute=59, second=59, microsecond=999999
    )

    # Calculate start and end of current day
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)

    # Calculate calories for the month
    calories_month = (
        FoodTrack.objects.filter(
            time__gte=start_of_month, time__lte=end_of_month
        ).aggregate(Sum("calorie"))["calorie__sum"]
        or 0
    )

    # Calculate calories for the day
    calories_day = (
        FoodTrack.objects.filter(time__gte=start_of_day, time__lte=end_of_day).aggregate(
            Sum("calorie")
        )["calorie__sum"]
        or 0
    )

    # Set calorie limits (you can adjust these values or make them dynamic)
    daily_calorie_limit = 2500  # Example daily limit
    monthly_calorie_limit = (
        daily_calorie_limit * last_day
    )  # Monthly limit based on days in month

    metrics = {
        "calories_month": calories_month,
        "calorie_limit_month": monthly_calorie_limit,
        "calories_day": calories_day,
        "calorie_limit_day": daily_calorie_limit,
    }

    if raw:
        return metrics
    else:
        return JsonResponse(metrics)
