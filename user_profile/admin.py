from django.contrib import admin
from user_profile.models import UserProfile,Site,Site_user
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Site)
admin.site.register(Site_user)