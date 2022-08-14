from urllib import response
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .models import User, Topic, Message
from datetime import datetime


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
                request.session['user'] = db_user.pk
                request.session['latest_activity'] = str(datetime.now())
                request.session.set_expiry(20)
                return HttpResponseRedirect("/home/")
            else:
                error = "Username or password incorrect."

    return render(request, 'index.html', {'error':error})


def home(request):
    request.session.clear_expired()
    try:
        username = request.session['username']
    except:
        response = HttpResponseRedirect("/")
        response.delete_cookie('sessionid')
        return response

    request.session['latest_activity'] = str(datetime.now())
    topics = Topic.objects.all()
    return render(request, 'home.html', {'topics':topics, 'username':username})

@csrf_protect
def new_topic(request):
    request.session.clear_expired()
    try:
        userid = request.session['user']
        user = User.objects.get(pk=userid)
    except:
        response = HttpResponseRedirect("/")
        response.delete_cookie('sessionid')
        return response
    error=""
    request.session['latest_activity'] = str(datetime.now())
    if request.method == "POST":
        #TODO:check lengths
        form_title = request.POST['title']
        form_text = request.POST['body']
        Topic.objects.create(title=form_title, text=form_text, poster=user, visible=True)
        return HttpResponseRedirect('/home/')
    return render(request, 'new_topic.html')

def logout(request):
    request.session.flush()
    return HttpResponseRedirect("/")

@csrf_protect
def topic(request, topic_id):
    request.session.clear_expired()
    try:
        user_id = request.session['user']
    except:
        response = HttpResponseRedirect("/")
        response.delete_cookie('sessionid')
        return response
    request.session['latest_activity'] = str(datetime.now())
    
    topic = get_object_or_404(Topic, pk=topic_id)
    messages = Message.objects.filter(topic=topic)
    if request.method == "POST":
        form_text = request.POST['comment']
        form_poster = User.objects.get(pk=user_id)
        Message.objects.create(text=form_text, poster=form_poster, topic=topic, visible=True)
        return HttpResponseRedirect(f"/topic/{topic_id}/")
    return render(request, 'topic.html', {'topic':topic, 'messages':messages})

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