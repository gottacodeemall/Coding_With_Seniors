from django.conf.urls import url

from . import views

app_name = "user"

urlpatterns = [
    url(r'^$', views.profile, name="profile"),
    url(r'^register/$', views.register, name="register"),
    url(r'^coding_accounts/$',views.coding_accounts, name="coding_accounts"),
    url(r'^login/$', views.login_user, name="login"),
    url(r'^logout/$', views.logout_user, name="logout"),
    url(r'^user_info/$', views.user_infos, name="user_infos")   
]