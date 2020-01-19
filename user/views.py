import requests, random, json
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

class ChartView(TemplateView):
    template_name = "user/chart.html"

def CalorieConversion(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            cur_weight = form.cleaned_data['cweight']
            des_weight = form.cleaned_data['dweight']

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
    name = form.cleaned_data['name'].split(' ')
    request.session["fname"] = name[0]
    request.session["lname"] = name[1]
    User(first_name = name[0],
     last_name = name[1],
     current_weight = cur_weight, desired_weight = des_weight,
     increment = abs_increment, protein = des_protein, carbs = des_carbs,
     fat = des_fat, email = form.cleaned_data['email'],
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
    remaining = 0
    person_data = User.objects.filter(first_name=request.session['fname'], last_name=request.session['lname'])
    if (person_data.desired_weight > person_data.current_weight): remaining = person_data.calorie + person_data.increment
    elif (person_data.desired_weight < person_data.current_weight): remaining = person_data.calorie - person_data.increment
    else: remaining = person_data.calorie

    arr = json.loads(user_choices)
    choice = []
     
    for item in arr:
        choice.append(str(item['serving_qty']) + ' ' + str(item['serving_unit']) + ' ' + item['food_name'])
        
    calories, fat, protein, carbs, lim = nutrient_req(choice, remaining)
    remaining = lim


    food = {
        "breakfast": ["2 large eggs", "3 oz ground turkey", "1 medium muffin", "1 cup oatmeal", "2 pancakes"],
        "protein": ["1 chicken breast", "1 steak", "1 fillet salmon", "1 fillet cod", "8 large shrimps"],
        "carbs": ["1 medium sweet potato", "1 cup rice", "1 medium potato", "1 cup quinoa", "1 cup brown rice"],
        "veg": ["2 cups spinach", "1 cup mixed vegetables", "2 cups chopped broccoli", "5 spears asparagus"],
        "fruits": ["6 large strawberry", "1 cup blackberry", "1 medium banana", "1 cup blueberry", "1 large apple"]
    }
    pack = {
        "2 large eggs": "12 pack eggs",
        "3 oz ground turkey": "1 pack ground turkey",
        "1 medium muffin": "6 pack muffins",
        "1 cup oatmeal": "1 pack oatmeal",
        "2 pancakes": "1 pack pancakes",
        "1 chicken breast": "1 pack chicken breasts",
        "1 steak": "1 pack steak",
        "1 fillet salmon": "1 pack salmon",
        "1 fillet cod": "1 pack cod",
        "8 large shrimps": "1 pack shrimp",
        "1 medium sweet potato": "2 medium sweet potato",
        "1 cup rice": "2 packs rice",
        "1 medium potato": "2 medium potatoes",
        "1 cup quinoa": "1 box quinoa",
        "1 cup brown rice": "2 packs brown rice",
        "2 cups spinach": "1 pack baby spinach",
        "1 cup mixed vegetables": "1 pack mixed vegetables",
        "2 cups chopped broccoli": "1 head of broccoli",
        "5 spears asparagus": "1 bundle of asparagus",
        "6 large strawberry": "1 pack strawberries",
        "1 cup blackberry": "1 pack blackberries",
        "1 medium banana": "1 hand of bananas",
        "1 cup blueberry": "1 pack of blueberries",
        "1 large apple": "3 large apples"
    }

    day = []
    random.shuffle(food["breakfast"])
    random.shuffle(food["protein"])
    random.shuffle(food["carbs"])
    random.shuffle(food["veg"])
    random.shuffle(food["fruits"])
    day = day + food["breakfast"][:2]
    day = day + food["protein"][:3]
    day = day + food["carbs"][:3]
    day = day + food["veg"][:3]
    day = day + food["fruits"][:2]
    random.shuffle(day)
    day = day + choice

    cal, ft, pro, cb, limit = nutrient_req(day, remaining)

    calories += cal
    fat += fat
    protein += pro
    carbs += cb

    grlist = []
    html = '<p>Hi ' + request.session['fname'] + ',</p></br>'
    html += "<p>Here is your weekly grocery shopping list:</p>"
    html += "<ul>"
    for item in day:
        grlist.append(pack[item])
        html += '<li>' + pack[item] + '</li>'
    html += "</ul></br><p>Enjoy,</p><p>Your friends at Fulfilled</p>"

    requests.get(
    'https://billwu95.api.stdlib.com/grocery@dev/emaillist/?html=' + html
    )

    context = {
        "calories": calories,
        "fat": fat,
        "carbs": carbs,
        "protein": protein,
        "grocery_list": grlist
    }

    return render(request, "user/food.html", context)


def data(request):
    response = redirect('/user/search-food/')
    return response


def nutrient_req(arr, limit):
    calories, fat, protein, carbs = 0, 0, 0, 0
    for item in arr:
        response = requests.post("https://trackapi.nutritionix.com/v2/natural/nutrients",
            headers = {
                "Content-Type": "application/json",
                "x-app-id": "728a7023",
                "x-app-key": "f8e3dbfdcbf2ed6634fc902128695159"
                },
            json = {
                'query': item,
                'timezone': "US/Eastern"
                }
        )
        text = response.json()['foods'][0]
        if (calories + text['nf_calories'] < limit):
            calories += text['nf_calories']
            fat += text['nf_total_fat']
            carbs += text['nf_total_carbohydrate']
            protein += text['nf_protein']
            limit -= text['nf_calories']
    return calories, fat, protein, carbs, limit
