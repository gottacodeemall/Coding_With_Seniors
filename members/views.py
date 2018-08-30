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

from user_profile.models import UserProfile,Site,Site_user
def view_all(request: HttpRequest) -> HttpResponse:
    try:
        query=UserProfile.objects.all().order_by('display_name')
        url='/members/'
    except:
        messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return render(request,'members/all_members.html',locals())

def individual_member(request: HttpRequest,name:str) -> HttpResponse:
    try:
        user=UserProfile.objects.get(display_name=name)
        site_user=Site_user.objects.filter(user_info=user)
    except:
        messages.add_message(request, messages.ERROR, 'Error Contact Admin')
    return render(request,'members/view_member.html',locals())




