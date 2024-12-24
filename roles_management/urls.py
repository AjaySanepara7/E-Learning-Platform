from django.urls import path
from roles_management import views
from django.contrib.auth.decorators import login_required


app_name = "roles_management"
urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("login_page", views.LoginPage.as_view(), name="login_page"),    
    path("signup_page", views.SignupPage.as_view(), name="signup_page"),    
    path("dashboard", views.Dashboard.as_view(), name="dashboard"),    
    
]