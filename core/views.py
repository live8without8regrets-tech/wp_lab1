from django.http import JsonResponse
from datetime import date


def info_view(request):
    today = date.today()
    new_year = date(today.year + 1, 1, 1)
    days_left = (new_year - today).days
    return JsonResponse({"days_before_new_year": days_left})