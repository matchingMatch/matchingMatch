from django.urls import path
from . import views

app_name ="matchingMatch"

urlpatterns = [
    path("match_register",views.match_register, name="match_register"),
]

