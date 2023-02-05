from django.urls import path
from . import views

app_name = "matchingMatch"

urlpatterns = [
    path("", views.main, name="main"),
    path("endOfGame/", views.endOfGame, name="endOfGame")
]
