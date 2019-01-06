from django.contrib import admin
from .models import Profile , Neighborhood ,  Business ,Update , Comment

admin.site.register(Profile)
admin.site.register(Neighborhood)
admin.site.register(Update)
admin.site.register(Comment)
admin.site.register(Business)