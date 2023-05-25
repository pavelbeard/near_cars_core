import os

import pandas

from celery import shared_task

from django.conf import settings
from django.db import transaction
from django.db.models import QuerySet

from near_cars import models

db = "default" if settings.DEBUG else "near_cars"

@shared_task
def load_data_to_location_table():
    try:
        if models.Location.objects.using(db).count() > 0:
            return True

        path = os.path.join(os.getcwd(), "core", "uszips.csv")
        dataframe = pandas.read_csv(path)

        columns = ['city', 'state_name', 'zip', 'lat', 'lng']

        dataframe = dataframe[columns].to_dict('records')

        with transaction.atomic():
            for data in dataframe:
                q = models.Location.objects.using(db).create(
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
        if models.Car.objects.using(db).count() > 0:
            return True
        path = os.path.join(os.getcwd(), "core", "near_cars_car.csv")
        dataframe = pandas.read_csv(path)

        columns = list(dataframe.columns)

        dataframe = dataframe[columns].to_dict('records')
        models.Car.objects.using(db).using(db).create(
            uuid=columns[0],
            carrying=columns[1],
            location_id=columns[2]
        ).save()

        with transaction.atomic():
            for data in dataframe:
                q = models.Car.objects.using(db).create(
                    uuid=data[columns[0]],
                    carrying=data[columns[1]],
                    location_id=data[columns[2]],
                )
                q.save()
        return True
    except:
        return False
