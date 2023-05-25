from drf_spectacular.utils import OpenApiResponse, OpenApiParameter, OpenApiTypes
from rest_framework import status
from rest_framework import serializers

from . import models


class LocationResponseSerializer(serializers.Serializer):
    class Meta:
        model = models.Location
        fields = "__all__"


class PayloadResponseSerializer(serializers.Serializer):
    location_pickup = LocationResponseSerializer(read_only=True)
    location_carry_on = LocationResponseSerializer(read_only=True)

    class Meta:
        model = models.Payload
        fields = "__all__"


class PostResponses:
    PAYLOAD = {
        status.HTTP_201_CREATED: PayloadResponseSerializer,
        status.HTTP_406_NOT_ACCEPTABLE: OpenApiResponse(
            response={"error": "not acceptable"},
            description="Данные не валидны"
        )
    }


class PostParams:
    PAYLOAD = [
        OpenApiParameter(name="location_pickup", type=int, required=True),
        OpenApiParameter(name="location_carry_on", type=int, required=True),
        OpenApiParameter(name="weight", type=int, required=True),
        OpenApiParameter(name="description", type=int),
    ]