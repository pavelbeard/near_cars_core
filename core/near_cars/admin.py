from django.contrib import admin

# Register your models here.

from . import models


@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    pass
