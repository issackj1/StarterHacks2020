from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse
import requests

class HomeView(TemplateView):
    template_name = "user/home.html"
