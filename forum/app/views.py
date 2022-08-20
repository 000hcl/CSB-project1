from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db import connection
from .models import User, Topic, Message
from datetime import datetime
#from werkzeug.security import generate_password_hash, check_password_hash
#import pwnedpasswords


#@csrf_protect
@csrf_exempt
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
            #if check_password_hash(db_password, form_password):
            if form_password == db_password:
                request.session['username'] = db_user.username
                request.session['user'] = db_user.pk
                request.session['latest_activity'] = str(datetime.now())
                request.session['moderator'] = db_user.moderator
                #request.session.set_expiry(20)
                return HttpResponseRedirect("/home/")
            else:
                error = "Username or password incorrect."

    return render(request, 'index.html', {'error':error})

#@csrf_protect
@csrf_exempt
def makemoderator(request, user_id):

    #if request.method == "POST":
    #fix involves also indenting all rows except the last one once
    #request.session.clear_expired()
    try:
        moderator_status = request.session['moderator']
    except:
        response = HttpResponseRedirect("/")
        #response.delete_cookie('sessionid')
        return response
    request.session['latest_activity'] = str(datetime.now())

    #if moderator_status:
    user = User.objects.filter(pk=user_id)
    user.update(moderator=True)

    return HttpResponseRedirect("/home/")

#@csrf_protect
#injection test example: [n' UNION SELECT password FROM app_user WHERE username LIKE 'sage]
#returns user sage's password
@csrf_exempt
def search(request):
    #request.session.clear_expired()
    try:
        moderator_status = request.session['moderator']
    except:
        response = HttpResponseRedirect("/")
        #response.delete_cookie('sessionid')
        return response
    cursor = connection.cursor()
    sql = "SELECT username FROM app_user WHERE username LIKE '"
    users_clean = []
    if request.method == "POST":
        query = request.POST['query']
        sql+=query
        sql+= "'"
        cursor.execute(sql)
        #cursor.execute("SELECT username FROM app_user WHERE username LIKE %s", [query])
        users = cursor.fetchall()

        
        for user in users:
            users_clean.append(user[0])
    request.session['latest_activity'] = str(datetime.now())
    return render(request, 'search.html', {'users':users_clean, 'moderator':moderator_status})

#@csrf_protect
@csrf_exempt
def user(request, username):
    try:
        user = User.objects.get(username=username)
        id = user.id
        user_mod = user.moderator
        moderator_status = request.session['moderator']
        
        title_count = Topic.objects.filter(poster=user).count()
        message_count = Message.objects.filter(poster=user).count()
    except:
        return HttpResponseRedirect("/home/")
    
    request.session['latest_activity'] = str(datetime.now())
    return render(request, 'user.html', {'username':username,
                                         'user_id':id,
                                         'posts':title_count,
                                         'replies':message_count,
                                         'user_mod':user_mod, 'moderator':moderator_status})

#@csrf_protect       
@csrf_exempt
def home(request):
    #request.session.clear_expired()
    try:
        username = request.session['username']
        moderator_status = request.session['moderator']
    except:
        response = HttpResponseRedirect("/")
        #response.delete_cookie('sessionid')
        return response

    request.session['latest_activity'] = str(datetime.now())
    topics = Topic.objects.all()
    return render(request, 'home.html', {'topics':topics, 'username':username, 'moderator':moderator_status})

#@csrf_protect
@csrf_exempt
def new_topic(request):
    #request.session.clear_expired()
    try:
        userid = request.session['user']
        user = User.objects.get(pk=userid)
    except:
        response = HttpResponseRedirect("/")
        #response.delete_cookie('sessionid')
        return response
    error=""
    request.session['latest_activity'] = str(datetime.now())
    if request.method == "POST":
        form_title = request.POST['title']
        form_text = request.POST['body']
        if len(form_text)==0 or len(form_title)==0:
            return HttpResponse("Missing title or text")
        if len(form_text)>1000 or len(form_title)>100:
            return HttpResponse("Title or text too long.")
        Topic.objects.create(title=form_title, text=form_text, poster=user, visible=True)
        return HttpResponseRedirect('/home/')
    return render(request, 'new_topic.html')

def logout(request):
    request.session.flush()
    return HttpResponseRedirect("/")

#@csrf_protect
@csrf_exempt
def topic(request, topic_id):
    #request.session.clear_expired()
    try:
        user_id = request.session['user']
    except:
        response = HttpResponseRedirect("/")
        #response.delete_cookie('sessionid')
        return response
    request.session['latest_activity'] = str(datetime.now())
    
    topic = get_object_or_404(Topic, pk=topic_id)
    messages = Message.objects.filter(topic=topic)
    if request.method == "POST":
        form_text = request.POST['comment']
        if len(form_text)==0:
            return HttpResponse("Please write a comment.")
        if len(form_text)>1000:
            return HttpResponse("Your comment is too long.")
        form_poster = User.objects.get(pk=user_id)
        Message.objects.create(text=form_text, poster=form_poster, topic=topic, visible=True)
        return HttpResponseRedirect(f"/topic/{topic_id}/")
    return render(request, 'topic.html', {'topic':topic, 'messages':messages})

@csrf_exempt
#@csrf_protect
def register(request):
    error = ""
    if request.method == "POST":
        form_username = request.POST['username']
        form_password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        db_user = User.objects.filter(username=form_username).count()
        
        if form_password != confirm_password:
            error += "ERROR: Passwords don't match. "
        
        if len(form_password) < 8:
            error += "ERROR: Password too short. "
        
        if len(form_username) == 0:
            error += "No username was given. "
        
        if len(form_username) > 20:
            error += "ERROR: Username is too long."
        
        if len(form_password) > 64:
            error += "ERROR: Password is too long. "
        
        #if pwnedpasswords.check(form_password, plain_text=True) >0:
        #    error += "ERROR: The password is compromised, please use another."
        
        if (db_user >0):
            error += "ERROR: Username is taken. "
        
        if error == "":
            #form_password = generate_password_hash(form_password)
            User.objects.create(username=form_username, password=form_password)
            return HttpResponseRedirect("/")

    return render(request, 'register.html', {'error': error})