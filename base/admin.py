from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Room)
admin.site.register(models.Topic)
admin.site.register(models.Message)
