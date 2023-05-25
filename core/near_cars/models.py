from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from near_cars.utils import car_id_generator, get_all_zip_codes


# Create your models here.
class Location(models.Model):
    zip_code = models.IntegerField(primary_key=True)
    city = models.CharField(max_length=256)
    state = models.CharField(max_length=256)
    longitude = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(180.0)])
    latitude = models.FloatField(validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)])

    def __str__(self):
        return f"{self.state}/{self.city}/{self.zip_code}"


class NearCarsUszip(models.Model):
    zip = models.IntegerField(primary_key=True)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state_id = models.TextField(blank=True, null=True)
    state_name = models.TextField(blank=True, null=True)
    zcta = models.TextField(blank=True, null=True)
    parent_zcta = models.TextField(blank=True, null=True)
    population = models.TextField(blank=True, null=True)
    density = models.TextField(blank=True, null=True)
    county_fips = models.IntegerField(blank=True, null=True)
    county_name = models.TextField(blank=True, null=True)
    county_weights = models.TextField(blank=True, null=True)
    county_names_all = models.TextField(blank=True, null=True)
    county_fips_all = models.TextField(blank=True, null=True)
    imprecise = models.TextField(blank=True, null=True)
    military = models.TextField(blank=True, null=True)
    timezone = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'near_cars_uszip'


class Car(models.Model):
    uuid = models.CharField(max_length=5, primary_key=True, default=car_id_generator)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, blank=True, null=True)
    carrying = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)])

    def __str__(self):
        return f"Car {self.uuid}/{self.location}"


class Payload(models.Model):
    # ZIP_CODES = get_all_zip_codes()

    location_pickup = models.ForeignKey(Location, related_name="location_pickup",
                                        # on_delete=models.SET_NULL, blank=True, null=True, choices=ZIP_CODES)
                                        on_delete=models.SET_NULL, blank=True, null=True)
    location_carry_on = models.ForeignKey(Location, related_name="location_carry_on",
                                          # on_delete=models.SET_NULL, blank=True, null=True, choices=ZIP_CODES)
                                          on_delete=models.SET_NULL, blank=True, null=True)
    weight = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)])
    description = models.TextField()

    def __str__(self):
        return f"Payload {self.id}/{self.description}"
