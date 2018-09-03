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
app_name="console"
from . import views
urlpatterns = [
    path('',views.console,name="edit"),
    path('add/session/<str:event_name>',views.add_session_view,name="add_session"),
    path('add/readingmaterial/<str:session_name>',views.add_reading_view,name="add_reading"),
    path('add/event',views.add_event_view,name="add_event"),
    path('add/problem/<str:session_name>',views.add_problem_view,name="add_problem"),
    path('add/ranking',views.add_event_view,name="add_ranking"),
    path('add/site',views.add_event_view,name="add_site"),
    path('add/tag',views.add_event_view,name="add_tag"),
    path('edit/problem/<str:problem_name>',views.edit_problem,name="edit_problem"),
    path('edit/readingmaterial/<str:reading_name>',views.edit_reading,name="edit_reading"),
    path('edit/event/<str:event_name>',views.edit_event,name="edit_event"),
    path('edit/session/<str:session_name>',views.edit_session,name="edit_session"),
    path('do_not_use/session/<str:session_name>',views.delete_session,name="delete_session"),
    path('do_not_use/event/<str:event_name>',views.delete_event,name="delete_event"),
    path('do_not_use/problem/<str:problem_name>',views.delete_problem,name="delete_problem"),
    path('update_leaderboard/<str:name>',views.update_leaderboard,name="update_leaderboard"),
    path('update_rating/<str:name>',views.update_rating,name="update_rating"),
    path('update_contributors',views.update_contributors,name="update_contributors"),
    path('delete_rank/<str:s_name>/<str:name>/<str:rank>',views.delete_rank,name="delete_rank")

]
