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
from home import views
urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^members/', include('members.urls', namespace='members')),
    url(r'^leaderboard/', include('leaderboard.urls', namespace='leaderboard')),
    url(r'^user/', include('user_profile.urls', namespace='user')),
    url(r'^events/', include('events.urls', namespace='events')),
    url(r'^console/', include('console.urls', namespace='console')),
    url(r'^admin/', admin.site.urls),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)