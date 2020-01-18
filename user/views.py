from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse

class HomeView(TemplateView):
    template_name = "user/home.html"

class DashboardView(TemplateView):
    template_name = "user/dashboard.html"
