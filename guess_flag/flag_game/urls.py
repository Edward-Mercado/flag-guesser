from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("marathon-mode-start/", views.marathon_mode, name="marathon_mode"),
    path("loser/", views.loser, name="loser"),
    path("marathon-mode/", views.verify_answer, name="verify_answer"),
    path("regular-game/", views.regular_game_processing, name="regular_game_processing"),
]