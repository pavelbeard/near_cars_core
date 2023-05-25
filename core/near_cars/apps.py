from django.apps import AppConfig

from celery import current_app


class NearCarsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'near_cars'

    def ready(self):
        current_app.send_task("near_cars.tasks.load_data_to_location_table")
        current_app.send_task("near_cars.tasks.load_cars")
