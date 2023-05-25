from django.conf import settings
from django.forms import model_to_dict
from drf_spectacular.utils import extend_schema
from geopy.distance import distance
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models
from . import serializers
from .doc_utils import PayloadResponseSerializer, PostParams, PostResponses

db = "default" if settings.DEBUG else "near_cars"


# Create your views here.

class PayloadViewset(viewsets.ModelViewSet):
    queryset = models.Payload.objects.using(db).all()
    serializer_class = serializers.PayloadSerializer
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
        payload_list = []
        for payload in self.queryset:
            point1 = (payload.location_pickup.latitude, payload.location_pickup.longitude)

            cars_count = []

            for car in models.Car.objects.using(db).all():
                point2 = (car.location.latitude, car.location.longitude)

                if distance(point1, point2).miles <= 450:
                    cars_count.append(True)

            serializer = self.serializer_class(data=model_to_dict(payload))

            if not serializer.is_valid():
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

            payload_list.append({
                "payload": serializer.data, "cars_count_near": len(cars_count)
            })

        return Response(payload_list, status.HTTP_200_OK)

    @extend_schema(summary="Вывести конкретный груз, с расстоянием от всех машин, а также с их номерами",
                   tags=["near_cars/get"],
                   request=serializers.PayloadSerializer,
                   responses={201: PayloadResponseSerializer})
    def retrieve(self, request, *args, **kwargs):
        payload = self.queryset.using(db).get(pk=int(kwargs.get('pk')))
        point1 = (payload.location_pickup.latitude, payload.location_pickup.longitude)

        serializer = self.serializer_class(data=model_to_dict(payload))

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        list_of_cars = []
        for car in models.Car.objects.using(db).all():
            point2 = (car.location.latitude, car.location.longitude)

            list_of_cars.append({
                "car_uuid": car.uuid,
                "distance": f"{distance(point1, point2).miles:.2f}"
            })

        return Response({"payload": serializer.data, "list_of_cars": list_of_cars}, status.HTTP_200_OK)


class CarViewset(viewsets.ModelViewSet):
    queryset = models.Car.objects.using(db).all()
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
    queryset = models.Location.objects.using(db).all()
    serializer_class = serializers.LocationSerializer
    permission_classes = (AllowAny, )