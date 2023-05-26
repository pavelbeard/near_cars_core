import os
import sys
import time

import pandas
from django.core.exceptions import ValidationError
from django.core.management import BaseCommand
from django.db import connections, transaction
from django.db.utils import OperationalError
from django.utils import timezone
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from near_cars import models

help_string = "Добавляет машины в БД из csv файла"

PATH_CSV = os.getenv('PATH_CSV', os.path.join(os.getcwd(), "core"))


class Command(BaseCommand):
    help = help_string

    def handle(self, *args, **options):
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

            self.stdout.write("success!")
        except Exception as e:
            self.stdout.write(e.args[0])
