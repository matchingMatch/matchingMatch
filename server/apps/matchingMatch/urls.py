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
    path('my_register_matches/<int:pk>', views.my_register_matches, name="my_register_matches"),
    path('my_apply_matches/<int:pk>', views.my_apply_matches, name="my_apply_matches"),
    path('match_detail/<int:pk>', views.match_detail, name="match_detail"),
    path('applying_team_list/<int:pk>',
         views.applying_team_list, name="applying_team_list"),
    path('match_detail/<int:pk>', views.match_detail, name="match_detail"),
    path('match_request/', views.match_request, name = "match_request"),
    path('match_cancel/', views.match_cancel, name = "match_cancel"),
    path('edit-account/', views.edit_account, name="edit-account"),
    path('change-password/', views.change_password, name="change-password"),
    path('change_enroll/', views.change_enroll, name='change_enroll'),
    path('team_list/', views.team_list, name ='team_list'),
    path('delete-account/<int:pk>', views.delete_account.as_view(), name="delete-account"),
    path('match_update/<int:pk>', views.match_update, name = "match_update"),
    path('match_delete/<int:pk>', views.match_delete, name = "match_delete"),
    path('team_detail/<int:pk>',  views.team_detail, name = "team_detail"),
    path('rate/<int:pk>', views.rate, name="rate"),
    path('match/ended/', views.check_endedmatch, name="check_endedmatch"),
]
