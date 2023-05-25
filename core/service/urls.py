from django.urls import path

from service import views

app_name = "service"

urlpatterns = (
    path("get_csrf", views.get_csrf, name="get_csrf"),
)