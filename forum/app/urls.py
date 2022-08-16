from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('new_topic/', views.new_topic, name='new topic'),
    path('topic/<int:topic_id>/', views.topic, name='topic'),
    path('makemoderator/<int:user_id>/', views.makemoderator, name='make mod'),
    path('logout/', views.logout, name='log out'),
    path('search/', views.search, name='search')
]
