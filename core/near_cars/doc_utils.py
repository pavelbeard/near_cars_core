from drf_spectacular import utils
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
        status.HTTP_406_NOT_ACCEPTABLE: utils.OpenApiResponse(
            response={"error": "not acceptable"},
            description="Данные не валидны"
        )
    }


class GetResponses:
    PAYLOAD = {
        status.HTTP_200_OK: utils.OpenApiExample(
            name="t",
            value={"t": "t"},
            description="aa"
        ),
        status.HTTP_406_NOT_ACCEPTABLE: {"t": "t"}
    }


class PostParams:
    PAYLOAD = [
        utils.OpenApiParameter(name="location_pickup", type=int, required=True),
        utils.OpenApiParameter(name="location_carry_on", type=int, required=True),
        utils.OpenApiParameter(name="weight", type=int, required=True),
        utils.OpenApiParameter(name="description", type=int),
    ]


class GetExamples:
    PAYLOAD = [
        utils.OpenApiExample(
            response_only=True,
            name="payload_detail",
            description="payload_detail",
            value={
                "payload": {
                    "location_pickup": {
                        "zip_code": 0,
                        "city": "",
                        "state": "",
                        "longitude": 0.0,
                        "latitude": 0.0
                    },
                    "location_carry_on": {
                        "zip_code": 0,
                        "city": "",
                        "state": "",
                        "longitude": 0.0,
                        "latitude": 0.0
                    },
                    "weight": 0,
                    "description": ""
                },
                "list_of_cars": [{
                    "car_uuid": "",
                    "distance": 0.0
                }]
            }
        ),
    ]
