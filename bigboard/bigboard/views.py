from django.template.loader import get_template
from django.http import HttpResponse
from django.shortcuts import render
import datetime

def hello(request):
    return render(request, 'base.html')

def current_datetime(request):
    now = datetime.datetime.now()
    return render(request, 'current_datetime.html', {'current_date': now})

def hunt(request, hunt_id):
    return render(request, 'base_hunt.html')
