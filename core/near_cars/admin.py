from django.contrib import admin

# Register your models here.

from . import models


@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Car)
class CarAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Payload)
class PayloadAdmin(admin.ModelAdmin):
    pass
