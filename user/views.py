import requests
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse
from .models import User

class HomeView(TemplateView):
    template_name = "user/home.html"

class DashboardView(TemplateView):
    template_name = "user/dashboard.html"
    
def CalorieConversion(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            cur_weight = form.cleaned_data['Current Weight']
            des_weight = form.cleaned_data['Desired Weight']

    des_protein = des_weight * 2.6
    des_carbs = des_weight * 2.6
    des_fat = des_weight
    cur_protein = cur_weight * 2.6
    cur_carbs = cur_weight * 2.6
    cur_fat = cur_weight

    cur_calorie = (cur_protein * 4) + (cur_carbs * 4) + (cur_fat * 9)
    des_calorie = (des_protein * 4) + (des_carbs * 4) + (des_fat * 9)
    # Absolute value divided by four, for a positive 4 week increment
    abs_increment = round(abs((cur_calorie - des_calorie) / 4), 0)

    User(first_name = form.cleaned_data['First Name'],
     last_name = form.cleaned_data['Last Name'],
     current_weight = cur_weight, desired_weight = des_weight,
     increment = abs_increment, protein = des_protein, carbs = des_carbs,
     fat = des_fat, email = form.cleaned_data['Email'],
     date=form.cleaned_data['Date']).save()
     
def search_box(input):
    response = requests.get(
        "https://trackapi.nutritionix.com/v2/search/instant?query=".append(input),
        headers={
            "x-app-id": "728a7023",
            "x-app-key": "f8e3dbfdcbf2ed6634fc902128695159"}
        )
    json_response = response.json()["common"][:5]
    return json_response

