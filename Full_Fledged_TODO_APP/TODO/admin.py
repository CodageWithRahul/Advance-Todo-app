from django.contrib import admin
from . models import Task,TaskInstance,UserDailyState

# Register your models here.
admin.site.register(Task)
admin.site.register(TaskInstance)
admin.site.register(UserDailyState)