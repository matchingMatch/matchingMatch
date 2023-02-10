from django.urls import path
from . import views
app_name = "matchingMatch"

urlpatterns = [
    path("match_register",views.match_register, name="match_register"),
    path("", views.main, name="main"),
    # Review : 일반적으로 도메인에 대문자는 잘 넣지 않습니다!
    path("endOfGame/", views.endOfGame, name="endOfGame"),
    path('login/', views.login_page, name="login"),
    path('register/', views.register_page, name="register"),
    path('logout/', views.logout_user, name="logout"),
    path('account/', views.account_page, name="account"),
    path('match_detail/<int:pk>', views.match_detail, name="match_detail"),
    path('match_request/', views.match_request, name = "match_request"),
    path('match_cancel/', views.match_cancel, name = "match_cancel"),
]
