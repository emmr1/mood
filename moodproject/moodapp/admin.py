from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserMood, UserStatistics

class UserMoodAdmin(admin.ModelAdmin):
    fields = ('mood','created','user','streak') 

admin.site.register(UserStatistics)
admin.site.register(UserMood, UserMoodAdmin)