import os, requests

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.models import User
