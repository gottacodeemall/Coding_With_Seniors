from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponseRedirect
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
from django.shortcuts import get_object_or_404
from django.utils import timezone
from events.models import Session
from user_profile.models import UserProfile
# Create your views here.
def home(request: HttpRequest):
    #try:
    now = timezone.now()
    upcoming = Session.objects.filter(date__gte=now).order_by('date')
    passed = Session.objects.filter(date__lt=now).order_by('-date')
    upzero=False
    if upcoming.count()==0:
        upzero=True
    if(passed):
        latestpassed=passed[0]
        tcod=latestpassed.top_coder
        tcont = latestpassed.top_contributor
        timp = latestpassed.top_improver
        if tcod is not None:
            u_tcod = get_object_or_404(UserProfile, display_name=tcod)
            tcodval=True
        else:
            tcodval=False
        if tcont is not None:
            u_tcont= get_object_or_404(UserProfile, display_name=tcont)
            tcontval=True
        else:
            tcont=False
        if timp is not None:
            u_timp = get_object_or_404(UserProfile, display_name=timp)
            timpval=True
        else:
            timpval=False
    #except:
       # messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return render(request, 'home/home.html', locals())