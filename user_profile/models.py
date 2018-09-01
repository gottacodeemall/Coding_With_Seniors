from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class UserProfile(models.Model):
    user_info= models.OneToOneField(User, on_delete=models.CASCADE)
    display_name=models.CharField(max_length=255, blank=True, null=True,unique=True)
    display_pic = models.URLField(default="https://cdn4.iconfinder.com/data/icons/ui-standard/96/People-512.png")
    reg_number=models.CharField(max_length=255, blank=True, null=True,unique=True)
    bio=models.CharField(max_length=255, blank=True, null=True)
    rating_change=models.IntegerField(default=0)
    normalized_rating=models.PositiveIntegerField(default=1200)

    def __str__(self) -> str:
        return str(self.user_info)

 #   def __init__(self, *args, **kwargs):
#       super().__init__(*args, **kwargs)
#        self.normalized_rating = 1200  # updated dynamically


class Site(models.Model):
    sitename=models.CharField(max_length=255,blank=False,null=True)
    def __str__(self) -> str:
        return str(self.sitename)

class Site_user(models.Model):
    username_on_site=models.CharField(max_length=255,blank=False,null=True)
    url=models.URLField(blank=False,null=True)
    sites=models.ForeignKey(Site,on_delete=models.CASCADE)
    user_info=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    def __str__(self) -> str:
        return "User "+str( self.username_on_site)+" on "+str(self.sites)


