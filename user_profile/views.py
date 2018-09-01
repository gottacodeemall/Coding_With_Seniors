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

from user_profile.forms import UserForm, UserProfileForm, LoginForm,CodingAccountForm
from user_profile.models import Site_user,Site
from events.models import PerSessionUserLikes,Session
#logger = logging.getLogger(__name__)


def create_or_update_user(request: HttpRequest, user_form: UserForm, user_profile_form: UserProfileForm, creating: bool) -> HttpResponse:
    if not user_form.is_valid() or not user_profile_form.is_valid():
        messages.add_message(request, messages.ERROR, user_form.non_field_errors())
    else:
        try:
            if creating:
                user = User.objects.create_user(username=user_form.cleaned_data['username'],
                                                email=user_form.cleaned_data['email'],
                                                password=user_form.cleaned_data['password'],
                                                is_active=True)
            else:
                user = user_form.instance
                user.username = user_form.cleaned_data['username']
                new_pass = user_form.cleaned_data.get('password')
                if new_pass:
                    user.set_password(new_pass)
                else:
                    user.password = user_form.initial['password']
                user.email = user_form.cleaned_data['email']
                user.save()
            user_profile = user_profile_form.save(commit=False)
            user_profile.user_info = user
            user_profile.save()
            if creating:
                sessionlist = Session.objects.all()
                for item in sessionlist:
                    persessionuserlikes = PerSessionUserLikes(user=user_profile,session=item)
                    persessionuserlikes.save()
                messages.add_message(request, messages.SUCCESS, 'Congratulations ! Your user is created.')
                t = authenticate(username=user.username, password=user_form.cleaned_data['password'])
                if t is not None:
                    login(request, t)
            else:
                messages.add_message(request, messages.SUCCESS, 'Your user has been updated.')
            return redirect(reverse('user:profile'))
        except Exception:
            #logger.exception('Error while creating/updating a user. creating=' + str(creating) + ', req=' + "\n".join(request.readlines()))
            messages.add_message(request, messages.ERROR, 'Error, Contact Admin')
    return None


@require_http_methods(["POST"])
@never_cache
@csrf_exempt
def logout_user(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        logout(request)
        messages.add_message(request, messages.INFO, "You've been logged out. Have a nice day.")
    else:
        messages.add_message(request, messages.ERROR, "Mmmh.. You have to be logged in to do this.")
    return redirect(reverse('user:login'))


@sensitive_post_parameters()
@csrf_protect
@never_cache
@require_http_methods(["GET", "POST"])
def register(request: HttpRequest) -> HttpResponse:
    if settings.REGISTER_ENABLED:
        if request.method == "POST":
            user_profile_form = UserProfileForm(request.POST, request.FILES)
            user_form = UserForm(request.POST)
            response = create_or_update_user(request, user_form, user_profile_form, True)
            if response is not None:
                return response
        else:
            user_profile_form = UserProfileForm()
            user_form = UserForm()
    else:
        messages.add_message(request, messages.ERROR, "You cannot register anymore, please contact an admin.")
    return render(request, 'user_profile/register.html', locals())


@sensitive_post_parameters()
@csrf_protect
@never_cache
@require_http_methods(["GET", "POST"])
def login_user(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name_or_email = login_form.cleaned_data['username_or_email']
            password = login_form.cleaned_data['password']
            user = authenticate(username=user_name_or_email, password=password)
            if user is None:
                user_by_mail = User.objects.filter(email=user_name_or_email)
                if user_by_mail and user_by_mail[0]:
                    username = user_by_mail[0].username
                    user = authenticate(username=username, password=password)
            if user is None:
                messages.add_message(request, messages.ERROR, 'Wrong user name or password. Please try again.')
            else:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, "You've been successfully logged in.")
                return redirect(request.GET.get('next', reverse('home')))
    else:
        login_form = LoginForm()
    return render(request, 'user_profile/login.html', locals())

@never_cache
@require_http_methods(["GET"])
def user_infos(request):
    resp = {
        "is_logged_in": request.user.is_authenticated,
        "is_admin": request.user.is_staff,
    }
    if request.user.is_authenticated:
        resp["pk"] = request.user.pk
    return JsonResponse(resp)


@login_required
@csrf_protect
@never_cache
@require_http_methods(["GET", "POST"])
def profile(request: HttpRequest) -> HttpResponse:
    user = request.user
    if not hasattr(user, 'userprofile'):
        messages.add_message(request, messages.ERROR, 'We tried really hard to find it but this user does not exists.')
        return redirect(reverse('user:login'))
    user_profile = user.userprofile

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        user_profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        response = create_or_update_user(request, user_form, user_profile_form, False)
        if response is not None:
            return response
    else:
        user_form = UserForm(instance=user)
        user_profile_form = UserProfileForm(instance=user_profile)

    return render(request, 'user_profile/profile.html', locals())


def update_user_coding_account(request: HttpRequest, coding_account_form: CodingAccountForm) -> HttpResponse:
    if not coding_account_form.is_valid():
        messages.add_message(request, messages.ERROR, coding_account_form.non_field_errors())
    else:
        try:
            
            user=request.user
            user_infos=user.userprofile
            site=Site_user(username_on_site=coding_account_form.cleaned_data['username_on_site'],
                           url=coding_account_form.cleaned_data['url'],
                           sites=Site.objects.get(sitename=coding_account_form.cleaned_data['sites']),
                           user_info=user_infos
                            )
            
            site.save()
            messages.add_message(request, messages.SUCCESS, 'Created Successfully.')
            return redirect(reverse('user:coding_accounts'))
        except Exception:
            #logger.exception('Error while creating/updating a user. creating=' + str(creating) + ', req=' + "\n".join(request.readlines()))
            messages.add_message(request, messages.ERROR, 'Sorry, an error occurred, please alert an admin.')
    return None

@login_required
@csrf_protect
@never_cache
@require_http_methods(["GET", "POST"])
def coding_accounts(request: HttpRequest) -> HttpResponse:
    user = request.user
    if not hasattr(user, 'userprofile'):
        messages.add_message(request, messages.ERROR, 'We tried really hard to find it but this user does not exists.')
        return redirect(reverse('user:login'))
    user_profile = user.userprofile
    queryforsites=Site_user.objects.filter(user_info=user_profile)
    if request.method == "POST":
        coding_account_form=CodingAccountForm(request.POST)
        queryforsites=Site_user.objects.filter(user_info=user_profile)
        response=update_user_coding_account(request, coding_account_form)
        if response is not None:
            return response
    else:
        coding_account_form=CodingAccountForm()
    return render(request, 'user_profile/add_coding_account.html', locals())

