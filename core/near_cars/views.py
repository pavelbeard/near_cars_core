from django.forms import model_to_dict
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular import utils
from drf_spectacular.utils import extend_schema, OpenApiExample, extend_schema_view
from geopy.distance import distance
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from . import doc_utils
from . import models, filters
from . import serializers


# Create your views here.

@extend_schema_view(
    list=extend_schema(
        summary="Получить список грузов",
        tags=['near_cars/gets'],
        examples=doc_utils.GetExamples.PAYLOAD
    ),
    create=extend_schema(
        summary="Создать груз",
        tags=["near_cars/posts"],
        request=serializers.PayloadSerializer,
        parameters=doc_utils.PostParams.PAYLOAD
    ),
    retrieve=extend_schema(
        summary="Вывести конкретный груз, с расстоянием от всех машин, а также с их номерами",
        tags=["near_cars/get"],
        request=serializers.PayloadSerializer,
        examples=doc_utils.GetExamples.PAYLOAD
    ),
    update=extend_schema(
        summary="Редактировать данные груза",
        tags=["near_cars/updates"]
    ),
    destroy=extend_schema(
        summary="Удалить груз",
        tags=["near_cars/deletes"],
    ),
    partial_update=extend_schema(
        exclude=True
    )
)
class PayloadViewset(viewsets.ModelViewSet):
    queryset = models.Payload.objects.all()
    serializer_class = serializers.PayloadSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.PayloadFilter
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        payload = serializer.save()
        serialize_payload = self.serializer_class(payload).data
        return Response({"status": serialize_payload}, status.HTTP_201_CREATED)

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

    def retrieve(self, request, *args, **kwargs):
        try:
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
        except self.queryset.model.DoesNotExist:
            return Response({"error": "model does not exists"}, status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            payload = self.queryset.get(pk=int(kwargs.get('pk')))
            payload.delete()
            return Response({"payload": "payload has been deleted"}, status.HTTP_204_NO_CONTENT)
        except self.queryset.model.DoesNotExist:
            return Response({"error": "payload does not exist"}, status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    list=extend_schema(exclude=True),
    create=extend_schema(exclude=True),
    retrieve=extend_schema(exclude=True),
    update=extend_schema(
        summary="Редактировать машину",
        tags=["near_cars/updates"]
    ),
    destroy=extend_schema(exclude=True),
    partial_update=extend_schema(exclude=True),
)
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


@extend_schema_view(
    list=extend_schema(exclude=True),
    create=extend_schema(exclude=True),
    retrieve=extend_schema(exclude=True),
    update=extend_schema(exclude=True),
    destroy=extend_schema(exclude=True),
    partial_update=extend_schema(exclude=True),
)
class LocationView(viewsets.ModelViewSet):
    queryset = models.Location.objects.all()
    serializer_class = serializers.LocationSerializer
    permission_classes = (AllowAny,)
