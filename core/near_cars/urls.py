from django.urls import path, include
from rest_framework import routers

from near_cars import views

app_name = "near_cars"

router = routers.DefaultRouter()

router.register("payload", views.PayloadViewset)
router.register("car", views.CarViewset)
router.register("location", views.LocationView)

urlpatterns = (
    path("", include(router.urls)),
)
