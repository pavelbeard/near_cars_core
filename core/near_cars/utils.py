import random

from django.conf import settings
from django.core.cache import cache
from django.db.models.base import ModelBase

from . import models


def car_id_generator():
    random_letter = chr(random.randint(65, 91))
    random_number = random.randint(1000, 10000)
    return f"{random_number}{random_letter}"


def get_all_zip_codes():
    zip_codes = cache.get('zip_codes_for_choices')
    if not zip_codes:
        cache.set('zip_codes_for_choices',
                  tuple((f"{loc.state}/{loc.city}/{loc.zip_code}", loc.zip_code)
                        for loc in models.Location.objects.all()),
                  70 * 20)
        zip_codes = cache.get('zip_codes_for_choices')

    return zip_codes or tuple()


def random_zip_code():
    zip_codes = cache.get('zip_codes')
    if not zip_codes:
        cache.set('zip_codes',
                  tuple(location.zip_code for location in models.Location.objects.all()),
                  70 * 20)
        zip_codes = cache.get('zip_codes')

    zip_code = random.choice(zip_codes)
    return zip_code


def list_to_qs(model, data):
    if not isinstance(model, ModelBase):
        raise ValueError(f"{model} must be be Model")

    if not isinstance(data, list):
        raise ValueError(f"{data} must be List Object")

    pk_list = [obj.pk for obj in data]
    qs = model.objects.filter(pk__in=pk_list)
    qs._result_cache = data
    return qs


