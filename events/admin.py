from django.contrib import admin
from .models import Event,Editorial,Session,Ranking,Problem,PerSessionUserLikes,Tags
# Register your models here.
admin.site.register(Event)
admin.site.register(Editorial)
admin.site.register(Session)
admin.site.register(Ranking)
admin.site.register(Problem)
admin.site.register(PerSessionUserLikes)
admin.site.register(Tags)
