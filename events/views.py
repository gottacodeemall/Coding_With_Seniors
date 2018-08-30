import logging

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from cws_site import settings

from .models import UserProfile,Event,Session

def view_events(request: HttpRequest) -> HttpResponse:
    try:
        query="all events"
    except:
        messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return render(request,'events/all_events.html',locals())

def view_event(request: HttpRequest,event_name:str) -> HttpResponse:
    try:
        query="one_event"
    except:
        messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return render(request,'events/all_events.html',locals())

def view_sessions(request: HttpRequest) -> HttpResponse:
    try:
        query = "all_sessions"
    except:
        messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return render(request, 'events/all_events.html', locals())

def view_session(request: HttpRequest,session_name:str) -> HttpResponse:
    try:
        query = "one_session"
    except:
        messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return render(request,'events/all_events.html',locals())










