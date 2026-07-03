from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def home(request):
    return HttpResponse('<h1>Welcome to my Django App!</h1>')

def about(request):
    return HttpResponse('<h1>About</h1><p>Built with Django.</p>')

def hello_world(request):
    return HttpResponse('Hello, World!')