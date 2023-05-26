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

help_string = "Добавляет локации в БД из csv файла"

PATH_CSV = os.getenv('PATH_CSV', os.path.join(os.getcwd(), "core"))


class Command(BaseCommand):
    help = help_string

    def handle(self, *args, **options):
        try:
            if models.Location.objects.count() > 0:
                self.stdout.write("table is filled")
                return

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

            self.stdout.write("success!")
        except Exception as e:
            self.stdout.write(e.args[0])
