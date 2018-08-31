"""cws_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
app_name="events"
from . import views
urlpatterns = [
    path('editorials/<str:name>',views.view_editorial,name="view_editorial"),
    path('add_editorial/<str:problem_name>',views.add_editorial,name="add_editorial"),
    path('like_editorial/<str:editorial_name>',views.like_editorial,name="like_editorial"),
    path('sessions',views.view_sessions, name="view_sessions"),
    path('problems',views.view_problems, name="view_problems"),
    path('problems/<str:problem_name>',views.view_problem, name="view_problem"),
    path('sessions/<str:session_name>',views.view_session, name="view_session"),
    path('', views.view_events, name="view_events"),
    path('<str:event_name>',views.view_event, name="view_event"),
]
