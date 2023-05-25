import random

from django.conf import settings
from django.core.cache import cache

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from . import models
from .utils import random_zip_code

db = "default" if settings.DEBUG else "near_cars"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        fields = ('city', 'state', 'zip_code', 'latitude', 'longitude')

    def create(self, validated_data):
        return models.Location.objects.using(db).create(**validated_data)


class PayloadSerializer(serializers.ModelSerializer):
    location_pickup = serializers.PrimaryKeyRelatedField(queryset=models.Location.objects.using(db).all())
    location_carry_on = serializers.PrimaryKeyRelatedField(queryset=models.Location.objects.using(db).all())
    car_distances = serializers.ListField()
    cars_count = serializers.IntegerField()

    class Meta:
        model = models.Payload
        fields = ('location_pickup', 'location_carry_on', 'weight', 'description', 'car_distances', 'cars_count')

    def create(self, validated_data):
        location_pickup = validated_data.pop('location_pickup')
        location_carry_on = validated_data.pop('location_carry_on')

        payload = models.Payload.objects.using(db).create(
            location_pickup=location_pickup,
            location_carry_on=location_carry_on,
            **validated_data
        )

        return payload

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        location_pickup = repr['location_pickup']
        location_carry_on = repr['location_carry_on']

        location_pickup = models.Location.objects.using(db).filter(zip_code=location_pickup).values().first()
        location_carry_on = models.Location.objects.using(db).filter(zip_code=location_carry_on).values().first()

        repr['location_pickup'] = location_pickup
        repr['location_carry_on'] = location_carry_on

        return repr


class CarSerializer(serializers.ModelSerializer):
    uuid = serializers.CharField(read_only=True)
    location = LocationSerializer(read_only=True)

    class Meta:
        model = models.Car
        fields = ('uuid', 'location', 'carrying')

    def create(self, validated_data):
        try:
            location = models.Location.objects.using(db).get(zip_code=random_zip_code())

            car = models.Car.objects.using(db).create(
                **validated_data,
                location=location
            )
            return car
        except models.Location.DoesNotExist:
            raise ValidationError({"location": "location does not exists"})
