import requests
import json
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse
from .models import User
from django.shortcuts import redirect

class HomeView(TemplateView):
    template_name = "user/home.html"

class AboutView(TemplateView):
     template_name = "user/about.html"

class DashboardView(TemplateView):
    template_name = "user/dashboard.html"

class SearchView(TemplateView):
    template_name = "user/search.html"
    

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
     date=form.cleaned_data['Date'],
     calorie=cur_calorie).save()
     
def search_box(request, input):
    response = requests.get(
        "https://trackapi.nutritionix.com/v2/search/instant?query=" + input,
        headers={
            "x-app-id": "728a7023",
            "x-app-key": "f8e3dbfdcbf2ed6634fc902128695159"}
        )
    json_response = response.json()["common"][:5]
    return JsonResponse(json_response, safe=False)

def FoodView(request, user_choices):
    calories, fat, protein, carbs = 0, 0, 0, 0
    arr = json.loads(user_choices)
    for item in arr:
        response = requests.post("https://trackapi.nutritionix.com/v2/natural/nutrients",
            headers = {
                "Content-Type": "application/json",
                "x-app-id": "728a7023",
                "x-app-key": "f8e3dbfdcbf2ed6634fc902128695159"
                },
            json = {
                'query': str(item['serving_qty']) + ' ' + 
                str(item['serving_unit'])
                + ' ' + item['food_name'], 'timezone': "US/Eastern"
                }
        )

        text = response.json()['foods'][0]
        calories += text['nf_calories']
        fat += text['nf_total_fat']
        carbs += text['nf_total_carbohydrate']
        protein += text['nf_protein']

    person_data = User.objects.filter(first_name=request.sessions['firstname'], last_name=request.sessions['lastname'])
    context = {
        "calories": calories,
        "fat": fat,
        "carbs": carbs,
        "protein": protein
    }
    remaining = 0

    if (person_data.desired_weight > person_data.current_weight) remaining = person_data.calorie + person_data.increment
    elif (person_data.desired_weight < person_data.current_weight)remaining = person_data.calorie - person_data.increment
    else remaining = person_data.calorie

    food = {
        "protein": ["1 chicken breast", "1 steak", "2 large eggs", "1 fillet salmon", "1 fillet cod"],
        "carbs": ["1 medium sweet potato", "1 cup rice", "1 medium potato", "1 cup quinoa", "1 cup brown rice"],
        "veg": ["2 cups spinach", "1 cup mixed vegetables", "2 cups chopped broccoli", "5 spears asparagus"],
        "fruits": ["6 large strawberry", "1 cup blackberry", "1 medium banana", "1 cup blueberry", "1 large apple"]
    }

def data(request):
    response = redirect('/food-search/')
    return response
