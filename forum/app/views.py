from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .models import User, Topic, Message


def index(request):
    return render(request, 'index.html')

@csrf_exempt
def register(request):
    error = ""
    if request.method == "POST":
        form_username = request.POST['username']
        form_password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        db_user = User.objects.filter(username=form_username).count()
        
        if form_password != confirm_password:
            error += "ERROR: Passwords don't match. "
        
        if len(form_password) == 0:
            error += "ERROR: No password was given. "
        
        if len(form_username) == 0:
            error += "No username was given. "
        
        if len(form_username) > 20:
            error += "ERROR: Username is too long."
        
        if len(form_password) > 20:
            error += "ERROR: Password is too long. "
        
        if (db_user >0):
            error += "ERROR: Username is taken. "
        
        if error == "":
            User.objects.create(username=form_username, password=form_password)
            return HttpResponseRedirect("/")

    return render(request, 'register.html', {'error':error})