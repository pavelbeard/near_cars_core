import os

import pandas
from celery import shared_task
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from . import models
from . import utils

PATH_CSV = os.getenv('PATH_CSV', os.path.join(os.getcwd(), "core"))

@shared_task
def load_data_to_location_table():
    try:
        if models.Location.objects.count() > 0:
            return True

        path = os.path.join(PATH_CSV, "uszips.csv")
        dataframe = pandas.read_csv(path)

        columns = ['city', 'state_name', 'zip', 'lat', 'lng']

        dataframe = dataframe[columns].to_dict('records')

        with transaction.atomic():
            for data in dataframe:
                q = models.Location.objects.create(
                    city=data['city'],
                    state=data['state_name'],
                    zip_code=data['zip'],
                    latitude=data['lat'],
                    longitude=data['lng'],
                )
                q.save()

        return True
    except:
        return False


@shared_task()
def load_cars():
    try:
        if models.Car.objects.count() > 0:
            return True
        path = os.path.join(PATH_CSV, "near_cars_car.csv")
        dataframe = pandas.read_csv(path)

        columns = list(dataframe.columns)

        dataframe = dataframe[columns].to_dict('records')
        models.Car.objects.create(
            uuid=columns[0],
            carrying=columns[1],
            location_id=columns[2]
        ).save()

        with transaction.atomic():
            for data in dataframe:
                q = models.Car.objects.create(
                    uuid=data[columns[0]],
                    carrying=data[columns[1]],
                    location_id=data[columns[2]],
                )
                q.save()
        return True
    except:
        return False


@shared_task()
def create_location_auto_update_task():
    try:
        interval, exists = IntervalSchedule.objects.get_or_create(every=10, period='seconds')
        task, exists = PeriodicTask.objects.get_or_create(
            name="Car location autoupdate",
            task="update_car_location_repeat",
            interval=interval,
            start_time=timezone.now()
        )
    except ValidationError:
        print("the task already exists")


@shared_task()
def update_car_location():
    cache.set('location_count', models.Location.objects.all(), 70 * 20)
    locations = cache.get('location_count')

    if locations.count() > 0:
        for car in models.Car.objects.all():
            car.location = locations.filter(zip_code=utils.random_zip_code()).first()
            car.save()
