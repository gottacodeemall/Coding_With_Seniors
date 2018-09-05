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
    try:
        now = timezone.now()
        upcomingall = Session.objects.filter(date__gte=now).order_by('date')
        upcoming=upcomingall[:5]
        passedall = Session.objects.filter(date__lt=now).order_by('-date')
        passed = passedall[:5]
        upzero=False
        if upcoming.count()==0:
            upzero=True
        if(passed):
            tcodbool=False
            timpbool=False
            tcontbool=False
            for item in passed:
                if item.top_coder and not tcodbool:
                    u_tcod=get_object_or_404(UserProfile, display_name=item.top_coder)
                    tcodbool=True
                    tcod_session=item.name
                if item.top_contributor and not tcontbool:
                    u_tcont=get_object_or_404(UserProfile, display_name=item.top_contributor)
                    tcontbool=True
                    tcont_session=item.name
                if item.top_improver and not timpbool:
                    u_timp=get_object_or_404(UserProfile, display_name=item.top_improver)
                    timpbool=True
                    timp_session=item.name
    except:
        messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return render(request, 'home/home.html', locals())