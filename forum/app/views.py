from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .models import User, Topic, Message


@csrf_protect
def index(request):
    error = ""
    
    if request.method == "POST":
        form_username = request.POST['username']
        form_password = request.POST['password']
        try:
            db_user = User.objects.get(username=form_username)
            
        except User.DoesNotExist:
            db_user = None
            error = "Username or password incorrect."
        if db_user is not None:
            db_password = db_user.password
            if form_password == db_password:
                request.session['username'] = db_user.username
                return HttpResponseRedirect("/home/")
            else:
                error = "Username or password incorrect."

    return render(request, 'index.html', {'error':error})


def home(request):
    try:
        username = request.session['username']
    except:
        return render(request, 'index.html', {'error': "Please log in first."})
    topics = Topic.objects.all()
    return render(request, 'home.html', {'topics':topics, 'username':username})
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

    return render(request, 'register.html', {'error': error})