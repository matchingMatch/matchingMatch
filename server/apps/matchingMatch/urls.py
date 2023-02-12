from django.urls import path
from . import views
app_name = "matchingMatch"

urlpatterns = [
    path("match_register", views.match_register, name="match_register"),
    path("", views.main, name="main"),
    path('login/', views.login_page, name="login"),
    path('register/', views.register_page, name="register"),
    path('logout/', views.logout_user, name="logout"),
    path('account/', views.account_page, name="account"),
    path('my_match_list/<int:pk>', views.my_match_list, name="my_match_list"),
    path('applying_team_list/<int:pk>',
         views.applying_team_list, name="applying_team_list"),
    path('match_detail/<int:pk>', views.match_detail, name="match_detail"),
    path('match_request/', views.match_request, name = "match_request"),
    path('match_cancel/', views.match_cancel, name = "match_cancel"),
    path('edit-account/', views.edit_account, name="edit-account"),
    path('change-password/', views.change_password, name="change-password"),
    path('change_enroll/', views.change_enroll, name='change_enroll'),
]
