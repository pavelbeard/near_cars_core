from django.conf import settings
from django.db.models import F
from django.forms import model_to_dict
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from geopy.distance import distance
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from . import models, filters
from . import serializers
from .doc_utils import PayloadResponseSerializer, PostParams, PostResponses


# Create your views here.

class PayloadViewset(viewsets.ModelViewSet):
    queryset = models.Payload.objects.all()
    serializer_class = serializers.PayloadSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = filters.PayloadFilter
    permission_classes = (AllowAny,)

    @extend_schema(summary="Создать груз",
                   tags=["near_cars/posts"],
                   parameters=PostParams.PAYLOAD,
                   request=serializers.PayloadSerializer,
                   responses=PostResponses.PAYLOAD)
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        payload = serializer.save()
        serialize_payload = self.serializer_class(payload).data
        return Response({"status": serialize_payload}, status.HTTP_201_CREATED)

    @extend_schema(summary="Вывести список грузов",
                   tags=["near_cars/get"],
                   request=serializers.PayloadSerializer,
                   responses={201: PayloadResponseSerializer})
    def list(self, request, *args, **kwargs):
        qs = self.filterset_class(request.query_params, self.get_queryset()).qs
        payload_list = []

        for o in qs:
            payload_list.append({
                'location_pickup': o.location_pickup.zip_code,
                'location_carry_on': o.location_carry_on.zip_code,
                'weight': o.weight,
                'description': o.description,
                'car_distances': getattr(o, 'car_distances', []),
                'cars_count': getattr(o, 'cars_count', 0)
            })

        serializer = self.serializer_class(data=payload_list, many=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status.HTTP_200_OK)

    @extend_schema(summary="Вывести конкретный груз, с расстоянием от всех машин, а также с их номерами",
                   tags=["near_cars/get"],
                   request=serializers.PayloadSerializer,
                   responses={201: PayloadResponseSerializer})
    def retrieve(self, request, *args, **kwargs):
        payload = self.queryset.get(pk=int(kwargs.get('pk')))
        point1 = (payload.location_pickup.latitude, payload.location_pickup.longitude)

        serializer = self.serializer_class(data=model_to_dict(payload))

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        list_of_cars = []
        for car in models.Car.objects.all():
            point2 = (car.location.latitude, car.location.longitude)

            list_of_cars.append({
                "car_uuid": car.uuid,
                "distance": f"{distance(point1, point2).miles:.2f}"
            })

        return Response({"payload": serializer.data, "list_of_cars": list_of_cars}, status.HTTP_200_OK)


class CarViewset(viewsets.ModelViewSet):
    queryset = models.Car.objects.all()
    serializer_class = serializers.CarSerializer
    permission_classes = (AllowAny,)

    @extend_schema(summary="Создать машину",
                   tags=["near_cars/posts"])
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        car = serializer.save()
        serializer_car = self.serializer_class(car).data
        return Response({"status": serializer_car}, status.HTTP_201_CREATED)


class LocationView(viewsets.ModelViewSet):
    queryset = models.Location.objects.all()
    serializer_class = serializers.LocationSerializer
    permission_classes = (AllowAny, )