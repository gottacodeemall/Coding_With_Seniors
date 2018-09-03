
from django.db import models
from django.utils import timezone
from user_profile.models import UserProfile
from django.contrib.auth.models import User

class Event(models.Model):
    name= models.CharField(max_length=255, blank=False, null=True,unique=True)
    date=models.DateField(blank=False, null=True)
    description=models.TextField( blank=False, null=True)

    def __str__(self) -> str:
        return str(self.name)


class Session(models.Model):
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    name=models.CharField(max_length=255, blank=False, null=True,unique=True)
    date=date=models.DateField(blank=False, null=True)
    description = models.TextField(blank=False, null=True)
    test_name=models.CharField(max_length=255,blank=True, null=True)
    test_url=models.URLField(blank=True, null=True)
    top_coder=models.CharField(max_length=255, blank=True, null=True)
    top_contributor=models.CharField(max_length=255, blank=True, null=True)
    top_improver=models.CharField(max_length=255, blank=True, null=True)
    rating_updated=models.BooleanField(default=False)
    def __str__(self) -> str:
        return '{0}'.format(self.name)

class PerSessionUserLikes(models.Model):
    count=models.PositiveIntegerField(default=0,null=True,blank=False)
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    session=models.ForeignKey(Session,on_delete=models.CASCADE)
    def __str__(self) -> str:
        return '{0} has {1} likes for {2} session'.format(self.user.display_name,self.count,self.session.name)

class Tags(models.Model):
    type=models.CharField(max_length=255,blank=False, null=True)
    def __str__(self) -> str:
        return '{0}'.format(self.type)

class Problem(models.Model):
    name=models.CharField(max_length=255, blank=False, null=True,unique=True)
    url_problem=models.URLField(blank=False, null=True)
    solution=models.CharField(max_length=255, blank=True, null=True)
    url_solution=models.URLField(blank=True, null=True)
    session=models.ForeignKey(Session,on_delete=models.CASCADE)
    tags=models.ManyToManyField(Tags,blank=True)
    def __str__(self) -> str:
        return '{0}'.format(self.name)

class Editorial(models.Model):
    name=models.CharField(max_length=255, blank=False, null=True,unique=True)
    user_submitted=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    problem=models.ForeignKey(Problem,on_delete=models.CASCADE)
    solution=models.TextField(blank=False,null=True)
    solution_url=models.URLField(blank=True,null=True)
    liked_users=models.ManyToManyField(User,blank=True)
    def __str__(self) -> str:
        return '{0} : {1}'.format(self.problem.name,self.user_submitted.display_name)


class Ranking(models.Model):
    rank = models.PositiveIntegerField(blank=False, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    class Meta:
        unique_together = ("rank", "user","session")
    def __str__(self) -> str:
        return '{0}: {1}'.format(self.rank, self.user.display_name)

class ReadingMaterial(models.Model):
    name=models.CharField(max_length=255, blank=False, null=True,unique=True)
    session=models.ForeignKey(Session, on_delete=models.CASCADE,default=None)
    type=models.CharField(max_length=255, blank=False, null=True)
    url=models.URLField(blank=True, null=True)
    def __str__(self) -> str:
        return '{0}'.format(self.name)
