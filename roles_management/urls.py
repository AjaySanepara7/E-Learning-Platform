from django.urls import path
from roles_management import views
from django.contrib.auth.decorators import login_required


app_name = "roles_management"
urlpatterns = [
    path("", views.Home.as_view(), name="home"),
       
    path("signup_page", views.SignupPage.as_view(), name="signup_page"),    
    
]