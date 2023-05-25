from copy import deepcopy

import django_filters
from django.db.models import QuerySet, F
from django.forms import model_to_dict
from geopy.distance import distance
from rest_framework.filters import BaseFilterBackend

from . import models, serializers
from .utils import list_to_qs


class DistanceFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        distance_value = float(request.query_params.get('distance', 0))

        filtered_qs = []
        for payload in queryset:
            point1 = payload.location_pickup.latitude, payload.location_pickup.longitude

            cars_count = []

            for car in models.Car.objects.all():
                point2 = car.location.latitude, car.location.longitude

                if distance(point1, point2).miles <= distance_value:
                    cars_count.append(True)

            if len(cars_count) > 0:
                filtered_qs.append(payload)

        return filtered_qs


class PayloadFilter(django_filters.FilterSet):
    weight = django_filters.NumberFilter(method="weight_filter")
    distance = django_filters.NumberFilter(method="distance_filter")

    class Meta:
        model = models.Payload
        fields = ('weight', 'distance')

    def weight_filter(self, queryset, name, value):
        if not value:
            return self.queryset

        return self.queryset.filter(weight__lte=int(value))

    def distance_filter(self, queryset, name, value):
        if not value:
            return self.queryset

        filtered_qs = []

        for payload in self.queryset.annotate(distance=F('weight'), cars_count=F('weight')):
            point1 = (payload.location_pickup.latitude, payload.location_pickup.longitude)

            cars_count = 0
            car_distances = []
            for car in models.Car.objects.all():
                location_pickup_distance = distance(point1, (car.location.latitude, car.location.longitude)).miles

                if location_pickup_distance <= float(value):
                    cars_count += 1
                    car_distances.append(location_pickup_distance)

            new_payload = deepcopy(payload)

            if not len(car_distances) == 0 and not cars_count == 0:
                new_payload.car_distances = car_distances
                new_payload.cars_count = cars_count
                filtered_qs.append(new_payload)

        qs = list_to_qs(models.Payload, filtered_qs)
        return qs
