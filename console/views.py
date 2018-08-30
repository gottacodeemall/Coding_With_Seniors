from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest,HttpResponseRedirect
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

from events.models import Ranking,Event,Session,Problem,Tags
from .forms import AddEventForm,AddSessionForm,AddProblemForm,RankForm
from user_profile.models import Site
# Create your views here.

def add_rank(request: HttpRequest, rank_form: RankForm,name:str) -> HttpResponse:
    if not rank_form.is_valid():
        messages.add_message(request, messages.ERROR, rank_form.non_field_errors())
    else:
        try:
            session = Session.objects.get(name=name)
            rank=Ranking(rank=rank_form.cleaned_data['rank'],user=rank_form.cleaned_data['user'],session=session)
            rank.save()
            messages.add_message(request, messages.SUCCESS, 'Rank Created')
            return redirect(reverse('console:update_leaderboard'))
        except Exception:
            # logger.exception('Error while creating/updating a user. creating=' + str(creating) + ', req=' + "\n".join(request.readlines()))
            messages.add_message(request, messages.ERROR, 'Sorry, an error occurred, please alert an admin.')
    return None

def update_leaderboard(request: HttpRequest,name:str):
    #try:
    session=Session.objects.get(name=name)
    ranks=Ranking.objects.filter(session=session).order_by('rank')
    if request.method == "POST":
        rank_form = RankForm(request.POST, instance=session)
        response = add_rank(request, rank_form, name)
        if response is not None:
            return response
    else:
        rank_form = RankForm()
    #except:
       # messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return render(request, 'console/console_ranking.html', locals())

def console(request: HttpRequest):
    try:
        events=Event.objects.all()
        sessions=Session.objects.all()
        problem=Problem.objects.all()
        tags=Tags.objects.all()
        site=Site.objects.all()
    except:
        messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return render(request,'console/edit.html',locals())

def add_session(request: HttpRequest, session_form: AddSessionForm,creating:bool,event_name:str) -> HttpResponse:
    if not session_form.is_valid():
        messages.add_message(request, messages.ERROR, session_form.non_field_errors())
    else:
        try:
            if(creating):
                eventid=Event.objects.get(name=event_name)
                session = Session(name=session_form.cleaned_data['name'],date=session_form.cleaned_data['date'],description=session_form.cleaned_data['description'],event=eventid,test_name=session_form.cleaned_data['test_name'],test_url=session_form.cleaned_data['test_url'])
                session.save()
                messages.add_message(request, messages.SUCCESS, 'Session Created')
            else:
                session=session_form.instance
                session.event=session_form.cleaned_data['event']
                session.name=session_form.cleaned_data['name']
                session.date = session_form.cleaned_data['date']
                session.description = session_form.cleaned_data['description']
                session.test_name = session_form.cleaned_data['test_name']
                session.test_url = session_form.cleaned_data['test_url']
                session.save()
                messages.add_message(request,messages.SUCCESS,'Session Updated')
            return HttpResponseRedirect("console/edit/event/{0}".format(event_name))
        except Exception:
            # logger.exception('Error while creating/updating a user. creating=' + str(creating) + ', req=' + "\n".join(request.readlines()))
            request.session['messages'] = ['Sorry, an error occurred, please alert an admin.']
    return None

def add_session_view(request:HttpRequest,event_name:str):
    try:
        add = True
        if request.method == "POST":
            session_form = AddSessionForm(request.POST)
            response = add_session(request, session_form,True,event_name)
            if response is not None:
                return response
        else:
            session_form = AddSessionForm()
    except:
        messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return render(request,'console/add_session.html',locals())

def add_event(request: HttpRequest, event_form: AddEventForm,creating:bool) -> HttpResponse:
    if not event_form.is_valid():
        messages.add_message(request, messages.ERROR, event_form.non_field_errors())
    else:
        try:
            if creating:
                event = Event(name=event_form.cleaned_data['name'],date=event_form.cleaned_data['date'],description=event_form.cleaned_data['description'])
                event.save()
                request.session['messages'] = ['Success on Event Creation']
            else:
                event = event_form.instance
                event.name = event_form.cleaned_data['name']
                event.date = event_form.cleaned_data['date']
                event.description = event_form.cleaned_data['description']
                event.save()
                request.session['messages'] = ['Event Updated']
            return redirect(reverse('console:edit'))
        except Exception:
            # logger.exception('Error while creating/updating a user. creating=' + str(creating) + ', req=' + "\n".join(request.readlines()))
            request.session['messages'] = ['Sorry, an error occurred, please alert an admin.']
    return None

def add_problem(request: HttpRequest, problem_form: AddProblemForm,creating:bool,session_name:str) -> HttpResponse:
    if not problem_form.is_valid():
        messages.add_message(request, messages.ERROR, problem_form.non_field_errors())
    else:
        try:
            session=Session.objects.get(name=session_name)
            if creating:
                problem = Problem(name=problem_form.cleaned_data['name'],
                                  url_problem=problem_form.cleaned_data['url_problem'],
                                  solution=problem_form.cleaned_data['solution'],
                                  url_solution=problem_form.cleaned_data['url_solution'],
                                  session=session)
                tags=problem_form.cleaned_data['tags']
                for item in tags:
                    problem.tags.add(item)
                problem.save()
                request.session['messages'] = ['Success on Event Creation']
            else:
                problem = problem_form.instance
                problem.name = problem_form.cleaned_data['name']
                problem.url_problem = problem_form.cleaned_data['url_problem']
                problem.solution = problem_form.cleaned_data['solution']
                problem.url_solution = problem_form.cleaned_data['url_solution']
                tags = problem_form.cleaned_data['tags']
                for item in tags:
                    problem.tags.add(item)
                problem.session = problem_form.cleaned_data['session']
                problem.save()
                request.session['messages'] = ['Event Updated']
            return HttpResponseRedirect("console/edit/session/{0}".format(session_name))
        except Exception:
            # logger.exception('Error while creating/updating a user. creating=' + str(creating) + ', req=' + "\n".join(request.readlines()))
            request.session['messages'] = ['Sorry, an error occurred, please alert an admin.']
    return None


def add_event_view(request:HttpRequest):
    try:
        add = True
        if request.method == "POST":
            event_form = AddEventForm(request.POST)
            response = add_event(request, event_form,True)
            if response is not None:
                return response
        else:
            event_form = AddEventForm()
    except:
        messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return render(request,'console/add_event.html',locals())

def add_problem_view(request:HttpRequest,session_name:str):
    try:
        add=True
        if request.method == "POST":
            problem_form = AddProblemForm(request.POST)
            response = add_problem(request, problem_form,True,session_name)
            if response is not None:
                return response
        else:
            problem_form = AddProblemForm()
    except:
        messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return render(request,'console/add_problem.html',locals())

def edit_event(request: HttpRequest,event_name:str):
    try:
        add = False
        event=Event.objects.get(name=event_name)
        if request.method == "POST":
            event_form=AddEventForm(request.POST, instance=event)
            response = add_event(request, event_form,False)
            if response is not None:
                return response
        else:
            event_form = AddEventForm(instance=event)
    except:
        messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return render(request,'console/add_event.html',locals())

def edit_problem(request: HttpRequest,problem_name:str):
    #try:
    add = False
    problem=Problem.objects.get(name=problem_name)
    if request.method == "POST":
        problem_form=AddProblemForm(request.POST, instance=problem)
        response = add_problem(request, problem_form,False,"null")
        if response is not None:
            return response
    else:
        problem_form = AddProblemForm(instance=problem)
    #except:
        #messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return render(request,'console/add_problem.html',locals())


def edit_session(request: HttpRequest,session_name:str):
    try:
        add=False
        session = Session.objects.get(name=session_name)
        problems=Problem.objects.filter(session=session)
        if request.method == "POST":
            session_form=AddSessionForm(request.POST, instance=session)
            response = add_session(request, session_form,False,"null")
            if response is not None:
                return response
        else:
            session_form = AddSessionForm(instance=session)
    except:
        messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return render(request,'console/add_session.html',locals())

def delete_session(request: HttpRequest,session_name:str):
    try:
        session = Session.objects.get(name=session_name)
        session.delete()
        messages.add_message(request, messages.SUCCESS, 'Deleted')
    except:
        messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return redirect(reverse('console:edit'))

def delete_event(request: HttpRequest,event_name:str):
    try:
        event = Event.objects.get(name=event_name)
        event.delete()
        messages.add_message(request, messages.SUCCESS, 'Deleted')
    except:
        messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return redirect(reverse('console:edit'))

def delete_problem(request: HttpRequest,problem_name:str):
    try:
        problem = Problem.objects.get(name=problem_name)
        problem.delete()
        messages.add_message(request, messages.SUCCESS, 'Deleted')
    except:
        messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return redirect(reverse('console:edit'))



