from celery import shared_task

import near_cars.management.commands.updatelocations as updatelocations


@shared_task()
def update_car_location():
    command = updatelocations.Command(print)
    command.handle()
