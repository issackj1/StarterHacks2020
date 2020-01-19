from django.urls import path, include
from django.views.generic import TemplateView

from . import views

app_name = 'user'

urlpatterns = [
    # ex: /user/
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('search/<str:input>/', views.search_box, name='search'),
    path('details/<str:user_choices>/', views.FoodView, name='data')
]