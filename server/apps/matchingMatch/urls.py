from django.urls import path
from . import views
app_name = "matchingMatch"

urlpatterns = [
    path("match_register",views.match_register, name="match_register"),
    path("", views.main, name="main"),
    path("endOfGame/", views.endOfGame, name="endOfGame"),
    path('login/', views.login_page, name="login"),
    path('register/', views.register_page, name="register"),
    path('logout/', views.logout_user, name="logout"),
    path('account/', views.account_page, name="account"),
    path('edit-account/', views.edit_account, name="edit-account"),
    path('change-password/', views.change_password, name="change-password"),
]