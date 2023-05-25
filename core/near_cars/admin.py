from django.contrib import admin

# Register your models here.

from . import models


@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Car)
class CarAdmin(admin.ModelAdmin):
    raw_id_fields = ('location',)


@admin.register(models.Payload)
class PayloadAdmin(admin.ModelAdmin):
    raw_id_fields = ('location_pickup', 'location_carry_on')
