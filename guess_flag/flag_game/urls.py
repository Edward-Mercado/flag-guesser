from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("/marathon-mode", views.marathon_mode, name="marathon_mode"),
    path("/loser", views.loser, name="loser")
]