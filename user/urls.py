from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls import url

from . import views

app_name = 'user'

urlpatterns = [
    # ex: /user/
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    # path('personaldata/', views.PersonalData.as_view(), name='personaldata'),
    url('data/', views.CalorieConversion, name='data'),
    path('search-food/', views.SearchView.as_view(), name='search-food'),
    path('search/<str:input>/', views.search_box, name='search'),
    path('chart/', views.ChartView.as_view(), name='chart'),
    path('details/<str:user_choices>/', views.FoodView, name='data'),
    path('email', views.email, name='email')

]
