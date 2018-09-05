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

from events.models import Ranking,Event,Session,Problem,Tags,PerSessionUserLikes,ReadingMaterial
from .forms import AddEventForm,AddSessionForm,AddProblemForm,RankForm,AddReadingForm
from user_profile.models import Site,UserProfile
# Create your views here.
@staff_member_required
@csrf_protect
@require_http_methods(["GET", "POST"])
def delete_rank(request: HttpRequest,s_name:str,name:str,rank:str):
    try:
        session=Session.objects.get(name=s_name)
        user_inst=User.objects.get(username=name)
        ranks=Ranking.objects.get(session=session,user=user_inst,rank=rank)
        ranks.delete()
        messages.add_message(request, messages.SUCCESS, 'Deleted')
    except:
        messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return HttpResponseRedirect("/console/update_leaderboard/{0}".format(s_name))

@staff_member_required
@sensitive_post_parameters()
@csrf_protect
@require_http_methods(["GET", "POST"])
def add_rank(request: HttpRequest, rank_form: RankForm,name:str) -> HttpResponse:
    if not rank_form.is_valid():
        messages.add_message(request, messages.ERROR, rank_form.non_field_errors())
    else:
        try:
            session = Session.objects.get(name=name)
            rank=Ranking(rank=rank_form.cleaned_data['rank'],user=rank_form.cleaned_data['user'],session=session)
            rank.save()
            messages.add_message(request, messages.SUCCESS, 'Rank Created')
            return HttpResponseRedirect("/console/update_leaderboard/{0}".format(name))
        except Exception:
            # logger.exception('Error while creating/updating a user. creating=' + str(creating) + ', req=' + "\n".join(request.readlines()))
            messages.add_message(request, messages.ERROR, 'Sorry, an error occurred, please alert an admin.')
            messages.add_message(request, messages.INFO, 'Check if row already exists in DB.')
    return None
@staff_member_required
@sensitive_post_parameters()
@csrf_protect
@require_http_methods(["GET", "POST"])
def update_leaderboard(request: HttpRequest,name:str):
    try:
        session=Session.objects.get(name=name)
        ranks=Ranking.objects.filter(session=session).order_by('rank')
        if request.method == "POST":
            rank_form = RankForm(request.POST)
            response = add_rank(request, rank_form, name)
            if response is not None:
                return response
        else:
            rank_form = RankForm()
    except:
        messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return render(request, 'console/console_ranking.html', locals())

@staff_member_required
@sensitive_post_parameters()
@csrf_protect
@require_http_methods(["GET", "POST"])
def console(request: HttpRequest):
    try:
        events=Event.objects.all().order_by('-date')
        sessions=Session.objects.all().order_by('-date')
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
            eventid = Event.objects.get(name=event_name)
            if(creating):

                session = Session(name=session_form.cleaned_data['name'],date=session_form.cleaned_data['date'],description=session_form.cleaned_data['description'],event=eventid,test_name=session_form.cleaned_data['test_name'],test_url=session_form.cleaned_data['test_url'])
                session.save()
                userset=UserProfile.objects.all()
                for userinst in userset:
                    likescount=PerSessionUserLikes(session=session,user=userinst)
                    likescount.save()
                messages.add_message(request, messages.SUCCESS, 'Session Created')
            else:
                session=session_form.instance
                session.name=session_form.cleaned_data['name']
                session.date = session_form.cleaned_data['date']
                session.description = session_form.cleaned_data['description']
                session.test_name = session_form.cleaned_data['test_name']
                session.test_url = session_form.cleaned_data['test_url']
                session.save()
                messages.add_message(request,messages.SUCCESS,'Session Updated')
            return HttpResponseRedirect("/console/edit/event/{0}".format(event_name))
        except Exception:
            # logger.exception('Error while creating/updating a user. creating=' + str(creating) + ', req=' + "\n".join(request.readlines()))
            messages.add_message(request, messages.ERROR, 'Sorry, an error occurred, please alert an admin.')
    return None
@staff_member_required
@sensitive_post_parameters()
@csrf_protect
@require_http_methods(["GET", "POST"])
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
                messages.add_message(request, messages.SUCCESS, "Event Created")
            else:
                event = event_form.instance
                event.name = event_form.cleaned_data['name']
                event.date = event_form.cleaned_data['date']
                event.description = event_form.cleaned_data['description']
                event.save()
                messages.add_message(request, messages.SUCCESS, "Event Updated")
            return redirect(reverse('console:edit'))
        except Exception:
            # logger.exception('Error while creating/updating a user. creating=' + str(creating) + ', req=' + "\n".join(request.readlines()))
            messages.add_message(request, messages.ERROR, 'Sorry, an error occurred, please alert an admin.')
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
                problem.save()
                for item in tags:
                    problem.tags.add(item)

                messages.add_message(request, messages.SUCCESS, "Problem Created")
            else:
                problem = problem_form.instance
                problem.name = problem_form.cleaned_data['name']
                problem.url_problem = problem_form.cleaned_data['url_problem']
                problem.solution = problem_form.cleaned_data['solution']
                problem.url_solution = problem_form.cleaned_data['url_solution']
                tags = problem_form.cleaned_data['tags']
                for item in tags:
                    problem.tags.add(item)
                problem.session = session
                problem.save()
                messages.add_message(request, messages.SUCCESS, "Problem Updated")
            return HttpResponseRedirect("/console/edit/session/{0}".format(session_name))
        except Exception:
            # logger.exception('Error while creating/updating a user. creating=' + str(creating) + ', req=' + "\n".join(request.readlines()))
            messages.add_message(request, messages.ERROR, 'Sorry, an error occurred, please alert an admin.')
    return None

@staff_member_required
@sensitive_post_parameters()
@csrf_protect
@require_http_methods(["GET", "POST"])
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

@staff_member_required
@sensitive_post_parameters()
@csrf_protect
@require_http_methods(["GET", "POST"])
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


def add_reading(request: HttpRequest, reading_form: AddReadingForm,creating:bool,session_name:str) -> HttpResponse:
    if not reading_form.is_valid():
        messages.add_message(request, messages.ERROR, reading_form.non_field_errors())
    else:
        try:
            session=Session.objects.get(name=session_name)
            if creating:
                reading = ReadingMaterial(name=reading_form.cleaned_data['name'],
                                  url=reading_form.cleaned_data['url'],
                                  type=reading_form.cleaned_data['type'],
                                  session=session)
                reading.save()
                messages.add_message(request, messages.SUCCESS, 'Material Created')
            else:
                reading = reading_form.instance
                reading.name = reading_form.cleaned_data['name']
                reading.url = reading_form.cleaned_data['url']
                reading.type = reading_form.cleaned_data['type']
                reading.session = session
                reading.save()
                messages.add_message(request, messages.SUCCESS, 'Material Updated')
            return HttpResponseRedirect("/console/edit/session/{0}".format(session_name))
        except Exception:
            # logger.exception('Error while creating/updating a user. creating=' + str(creating) + ', req=' + "\n".join(request.readlines()))
            messages.add_message(request, messages.ERROR, 'Sorry, an error occurred, please alert an admin.')
    return None

@staff_member_required
@sensitive_post_parameters()
@csrf_protect
@require_http_methods(["GET", "POST"])
def add_reading_view(request:HttpRequest,session_name:str):
    try:
        add=True
        if request.method == "POST":
            reading_form = AddReadingForm(request.POST)
            response = add_reading(request, reading_form,True,session_name)
            if response is not None:
                return response
        else:
            reading_form = AddReadingForm()
    except:
        messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return render(request,'console/add_reading.html',locals())

@staff_member_required
@sensitive_post_parameters()
@csrf_protect
@require_http_methods(["GET", "POST"])
def edit_reading(request: HttpRequest,reading_name:str):
    try:
        add = False
        reading=ReadingMaterial.objects.get(name=reading_name)
        if request.method == "POST":
            reading_form=AddReadingForm(request.POST, instance=reading)
            response = add_reading(request, reading_form,False,reading.session)
            if response is not None:
                return response
        else:
            reading_form = AddReadingForm(instance=reading)
    except:
        messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return render(request,'console/add_reading.html',locals())

@staff_member_required
@sensitive_post_parameters()
@csrf_protect
@require_http_methods(["GET", "POST"])
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

@staff_member_required
@sensitive_post_parameters()
@csrf_protect
@require_http_methods(["GET", "POST"])
def edit_problem(request: HttpRequest,problem_name:str):
    try:
        add = False
        problem=Problem.objects.get(name=problem_name)
        if request.method == "POST":
            problem_form=AddProblemForm(request.POST, instance=problem)
            response = add_problem(request, problem_form,False,problem.session)
            if response is not None:
                return response
        else:
            problem_form = AddProblemForm(instance=problem)
    except:
        messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return render(request,'console/add_problem.html',locals())

@staff_member_required
@sensitive_post_parameters()
@csrf_protect
@require_http_methods(["GET", "POST"])
def edit_session(request: HttpRequest,session_name:str):
    try:
        add=False
        session = Session.objects.get(name=session_name)
        problems=Problem.objects.filter(session=session)
        readingmaterial=ReadingMaterial.objects.filter(session=session)
        if request.method == "POST":
            session_form=AddSessionForm(request.POST, instance=session)
            response = add_session(request, session_form,False,session.event)
            if response is not None:
                return response
        else:
            session_form = AddSessionForm(instance=session)
    except:
        messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return render(request,'console/add_session.html',locals())

@staff_member_required
@sensitive_post_parameters()
@csrf_protect
@require_http_methods(["GET", "POST"])
def delete_session(request: HttpRequest,session_name:str):
    try:
        session = Session.objects.get(name=session_name)
        session.delete()
        messages.add_message(request, messages.SUCCESS, 'Deleted')
    except:
        messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return redirect(reverse('console:edit'))

@staff_member_required
@sensitive_post_parameters()
@csrf_protect
@require_http_methods(["GET", "POST"])
def delete_event(request: HttpRequest,event_name:str):
    try:
        event = Event.objects.get(name=event_name)
        event.delete()
        messages.add_message(request, messages.SUCCESS, 'Deleted')
    except:
        messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return redirect(reverse('console:edit'))

@staff_member_required
@sensitive_post_parameters()
@csrf_protect
@require_http_methods(["GET", "POST"])
def delete_problem(request: HttpRequest,problem_name:str):
    try:
        problem = Problem.objects.get(name=problem_name)
        problem.delete()
        messages.add_message(request, messages.SUCCESS, 'Deleted')
    except:
        messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return redirect(reverse('console:edit'))

import math
def probability(rating1,rating2):
    return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400))

@staff_member_required
@sensitive_post_parameters()
@csrf_protect
@require_http_methods(["GET", "POST"])
def update_rating(request: HttpRequest,name:str):
    try:
        session = Session.objects.get(name=name)
        if not session.rating_updated:
            ranks = Ranking.objects.filter(session=session).order_by('rank')
            init_rating=[]
            all_users=User.objects.all()
            participated_users=[]
            for item in ranks:
                participated_users.append(item.user)
            idle_users=list(set(all_users) - set(participated_users))

            for item in ranks:
                init_rating.append(item.user.userprofile.normalized_rating)
            main=[]
            total=ranks.count()
            for i in range(total):
                inside=[]
                main.append(inside)

            for i in range(total):
                for j in range(i+1,total):
                    proba=probability(init_rating[i],init_rating[j])
                    probb = probability(init_rating[j], init_rating[i])
                    mod_a=init_rating[i]+200*(proba)
                    mod_b=init_rating[j]-200*(1-probb)
                    main[i].append(mod_a)
                    main[j].append(mod_b)

            final_rating=[]
            for i in range(total):
                sum=0.0
                leng=len(main[i])
                for j in range(leng):
                    sum+=main[i][j]
                avg=sum/float(leng)
                if avg>2200:
                    avg=2200
                elif avg<200:
                    avg=200
                final_rating.append(avg)
            rating_change=[]
            max_change=-400.0 #change this when you alter the value of K in Elo
            element=-1
            for i in range(total):
                cur_change = final_rating[i] - init_rating[i]
                rating_change.append(cur_change)
                if(cur_change>=max_change):
                    element=i
                    max_change=cur_change

            i=0
            for item in ranks:
                userprofin=item.user.userprofile
                userprofin.normalized_rating=final_rating[i]
                userprofin.rating_change=rating_change[i]
                userprofin.save()
                i=i+1

            for item in idle_users:
                userprofin = item.userprofile
                userprofin.rating_change=0
                userprofin.save()
            userprofin = ranks[element].user.userprofile
            session.top_improver = userprofin.display_name
            userprofin = ranks[0].user.userprofile
            session.top_coder=userprofin.display_name
            session.rating_updated=True
            session.save()
            messages.add_message(request, messages.SUCCESS, 'Leaderboard,Top Coder, Top Improver Updated')
        else:
            messages.add_message(request, messages.ERROR, 'Rating has already been updated.')
    except:
        messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return redirect(reverse('leaderboard:view_leaderboard'))


@staff_member_required
@sensitive_post_parameters()
@csrf_protect
@require_http_methods(["GET", "POST"])
def update_contributors(request:HttpRequest):
    try:
        sessionset=Session.objects.all()
        for session in sessionset:
            userset=UserProfile.objects.all()
            max_likes_count=0
            top_contri=None
            for userinst in userset:
                user_likes=PerSessionUserLikes.objects.get(session=session,user=userinst)
                likes=user_likes.count
                if(likes>max_likes_count):
                    top_contri=userinst
                    max_likes_count=likes
            if top_contri is not None:
                session.top_contributor=top_contri.display_name
            session.save()
        messages.add_message(request, messages.SUCCESS, 'Updated Contributors')
    except:
        messages.add_message(request, messages.ERROR, 'Error, Contact Developer')


    return redirect(reverse('leaderboard:view_leaderboard'))



