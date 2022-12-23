from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("templates/weather", views.weather, name='weather'),
    path("templates/wea_db", views.wea_db, name='wea_db')
]