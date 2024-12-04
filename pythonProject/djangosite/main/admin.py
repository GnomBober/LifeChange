from django.contrib import admin

from .models import Course, Profile, Module

admin.site.register(Course)
admin.site.register(Profile)
admin.site.register(Module)