import json
import os

from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status

from near_cars.utils import car_id_generator, get_all_zip_codes, random_zip_code
from . import models
from . import tasks


# Create your tests here.


class CeleryTasksTests(TestCase):
    databases = {"near_cars", "default"}

    def test_load_data_to_location_table(self):
        result = tasks.load_data_to_location_table()
        self.assertEqual(result, True)


class TestNearCars(TestCase):
    databases = {"default", "near_cars"}

    fixtures = {"location.json", "car.json"}

    @staticmethod
    def load_fixture_data():
        fixture_data = cache.get('fixture_data_new')
        if not fixture_data:
            with open(os.path.join(os.getcwd().replace("core", ""), "core", "near_cars", "fixtures", "location.json"),
                      'r') as f:
                fd = json.loads(f.read())
                for f in fd:
                    models.Location.objects.create(
                        zip_code=f['pk'],
                        **f['fields']
                    ).save()

                objects = models.Location.objects.all()
                cache.set('fixture_data_new',
                          tuple(location.zip_code for location in objects),
                          70 * 20)
                fixture_data = cache.get('fixture_data_new')
        return fixture_data

    def setUp(self) -> None:
        # self.payload_query_set = self.load_fixture_data()
        self.create_payload_data = {
            "location_pickup": random_zip_code(),
            "location_carry_on": random_zip_code(),
            "weight": 1000,
            "description": "bla bla bla"
        }


    def test_create_payload_data(self):
        response = self.client.post(reverse("near_cars:create_payload"),
                                    data=self.create_payload_data)
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_utils(self):
        print(car_id_generator())

    def test_check_constraints_location(self):
        q = models.Location.objects.create(
            city="test",
            state="test",
            zip_code="900",
            longitude=-0.9,
            latitude=190,
        )

        try:
            q.full_clean()
            q.save()
        except ValidationError as e:
            print(e)

    def test_get_all_zip_codes(self):
        choices = get_all_zip_codes()
        print(choices)
        self.assertIsInstance(choices, tuple)

    @override_settings(DEBUG=True)
    def test_create_payload(self):
        response = self.client.post(reverse("near_cars:create_payload"), data=self.create_payload_data,
                                    content_type="application/json")
        print(response.status_code)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @override_settings(DEBUG=True)
    def test_get_payload_list(self):
        response = self.client.get(reverse("near_cars:create_payload"))
        print(response)
        pass

