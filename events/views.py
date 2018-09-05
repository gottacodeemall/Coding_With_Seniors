import logging

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.http import HttpResponse,HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from cws_site import settings

from .models import UserProfile,Event,Session,Problem,Editorial,PerSessionUserLikes,ReadingMaterial,Ranking
from .forms import AddEditorialForm


def view_events(request: HttpRequest) -> HttpResponse:
    try:
        eventset=Event.objects.all().order_by('-date')
        upzero=False
        if eventset.count()==0:
            upzero=True
    except:
        messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return render(request,'events/all_events.html',locals())

def view_event(request: HttpRequest,event_name:str) -> HttpResponse:
    try:
        event=Event.objects.get(name=event_name)
        session_set=Session.objects.filter(event=event)
    except:
        messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return render(request,'events/event.html',locals())

def view_sessions(request: HttpRequest) -> HttpResponse:
    try:
        sessionset = Session.objects.all().order_by('-date')
        upzero = False
        if sessionset.count() == 0:
            upzero = True
    except:
        messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return render(request, 'events/all_sessions.html', locals())

def view_session(request: HttpRequest,session_name:str) -> HttpResponse:
    try:
        session = Session.objects.get(name=session_name)
        problem_set=Problem.objects.filter(session=session)
        material_set=ReadingMaterial.objects.filter(session=session)
        ranks=Ranking.objects.filter(session=session).order_by('rank')
    except:
        messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return render(request,'events/session.html',locals())

def view_problems(request: HttpRequest) -> HttpResponse:
    try:
        problem_set = Problem.objects.all()
        upzero = False
        if problem_set.count() == 0:
            upzero = True
    except:
        messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return render(request, 'events/all_problems.html', locals())

def view_problem(request: HttpRequest,problem_name:str) -> HttpResponse:
    try:
        problem=Problem.objects.get(name=problem_name)
        editorialset=Editorial.objects.filter(problem=problem).order_by()
        tags=problem.tags.all()
    except:
        messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return render(request,'events/problem.html',locals())

def view_editorial(request: HttpRequest,name:str):
    try:
        editorial=Editorial.objects.get(name=name)
    except:
        messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return render(request,'events/editorial.html',locals())

@login_required
@sensitive_post_parameters()
@csrf_protect
@require_http_methods(["GET", "POST"])
def add_editorial(request: HttpRequest,problem_name:str):
    try:
        problem=Problem.objects.get(name=problem_name)
        user_submit=request.user.userprofile
        if request.method == "POST":
            editorial_form = AddEditorialForm(request.POST)
            if not editorial_form.is_valid():
                messages.add_message(request, messages.ERROR, editorial_form.non_field_errors())
            else:
                editorial=Editorial(problem=problem,user_submitted=user_submit,name=editorial_form.cleaned_data['name'],
                                    solution=editorial_form.cleaned_data['solution'],
                                    solution_url=editorial_form.cleaned_data['solution_url'])
                editorial.save()
                messages.add_message(request, messages.SUCCESS, 'Editorial Added')
                return HttpResponseRedirect("/events/problems/{0}".format(problem_name))
        else:
            editorial_form = AddEditorialForm()
    except:
        messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return render(request,'events/add_editorial.html',locals())

@login_required
@sensitive_post_parameters()
@csrf_protect
@never_cache
@require_http_methods(["GET", "POST"])
def like_editorial(request: HttpRequest,editorial_name:str):
    try:
        editorial=Editorial.objects.get(name=editorial_name)
        problem=editorial.problem
        session=problem.session
        userprof=UserProfile.objects.get(user_info=request.user)
        user=request.user
        liked_users=editorial.liked_users.all()
        if user in liked_users:
            messages.add_message(request, messages.INFO, 'You have already liked this Editorial')
        elif user.userprofile == editorial.user_submitted:
            messages.add_message(request, messages.ERROR, 'You cannot like your own editorial.')
        else:
            editorial.liked_users.add(request.user)
            editorial.save()
            persessionuserlikes=PerSessionUserLikes.objects.get(user=editorial.user_submitted,session=session)
            persessionuserlikes.count=persessionuserlikes.count+1
            persessionuserlikes.save()
            messages.add_message(request, messages.SUCCESS, 'Liked the Editorial')
            return HttpResponseRedirect("/events/problems/{0}".format(problem.name))
    except:
        messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return render(request,'events/editorial.html',locals())











