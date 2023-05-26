from django.core.cache import cache
from django.core.management import BaseCommand

from near_cars import models, utils

help_string = "Обновляет локации у машин случайным образом"


class Command(BaseCommand):
    help = help_string

    def handle(self, *args, **options):
        try:
            cache.set('location_count', models.Location.objects.all(), 70 * 20)
            locations = cache.get('location_count')
            print(locations)

            if locations.count() > 0:
                for car in models.Car.objects.all():
                    print(car)
                    car.location = locations.filter(zip_code=utils.random_zip_code()).first()
                    car.save()
        except Exception as e:
            self.stdout.write(e.args[0])
