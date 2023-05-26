import sys
import time

from django.core.exceptions import ValidationError
from django.core.management import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
from django.utils import timezone
from django_celery_beat.models import IntervalSchedule, PeriodicTask

help_string = "Создает задачу обновления локаций у машин"


class Command(BaseCommand):
    help = help_string

    def handle(self, *args, **options):
        try:
            interval, exists = IntervalSchedule.objects.get_or_create(every=10, period='seconds')
            # load_locations_task, exists = PeriodicTask.objects.get_or_create(
            #     name="Load locations",
            #     task="near_cars.tasks.load_locations",
            #     interval=interval,
            #     one_off=True,
            #     start_time=timezone.now()
            # )
            # load_cars_task, exists = PeriodicTask.objects.get_or_create(
            #     name="Load cars",
            #     task="near_cars.tasks.load_cars",
            #     interval=interval,
            #     one_off=True,
            #     start_time=timezone.now()
            # )
            autoupdate_task, exists = PeriodicTask.objects.get_or_create(
                name="Car location autoupdate",
                task="near_cars.tasks.update_car_location",
                interval=interval,
                start_time=timezone.now()
            )

            self.stdout.write(f"{interval, autoupdate_task}")
        except ValidationError:
            self.stdout.write('the task already exists')
        except Exception as e:
            self.stdout.write(e.args[0])