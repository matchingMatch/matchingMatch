from django.urls import path
from . import views
app_name = "matchingMatch"

urlpatterns = [
    path("match_register", views.match_register, name="match_register"),
    path("", views.main, name="main"),
    path("endOfGame/", views.endOfGame, name="endOfGame"),
    path('login/', views.login_page, name="login"),
    path('register/', views.register_page, name="register"),
    path('logout/', views.logout_user, name="logout"),
    path('account/', views.account_page, name="account"),
    path('my_register_matches/<int:pk>', views.my_register_matches, name="my_register_matches"),
    path('my_apply_matches/<int:pk>', views.my_apply_matches, name="my_apply_matches"),
    path('match_detail/<int:pk>', views.match_detail, name="match_detail"),
    path('applying_team_list/<int:pk>',
         views.applying_team_list, name="applying_team_list"),
]
