from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')

def register(request):
    return HttpResponse('Register')