from django.contrib import admin
from .models import Profile , Neighborhood , PolicePost , Business , Hospital ,Update , Comment

admin.site.register(Profile)
admin.site.register(Neighborhood)
admin.site.register(PolicePost)
admin.site.register(Business)
admin.site.register(Hospital)

admin.site.register(Update)
admin.site.register(Comment)