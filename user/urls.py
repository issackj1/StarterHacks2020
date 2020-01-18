from django.urls import path, include
from django.views.generic import TemplateView

from . import views

app_name = 'user'

urlpatterns = [
    # ex: /user/
    path('', views.HomeView.as_view(), name='home'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard')
]