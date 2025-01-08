from django.urls import path, re_path
from django.views.generic import RedirectView
from roles_management import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


app_name = "roles_management"
urlpatterns = [
    re_path(r'^favicon\.ico$', RedirectView.as_view(url='/static/Assets/img/favicon.png')),
    path("", views.Login.as_view(), name="login"),
    path("course", views.CourseView.as_view(), name="course"),
    path("signup", views.Signup.as_view(), name="signup"),    
    path("logout", views.Logout.as_view(), name="logout"),    
    path("dashboard", login_required(views.Dashboard.as_view()), name="dashboard"),    
    path("profile", login_required(views.ProfileView.as_view()), name="profile"),    
    path("enroll/<int:course_id>", login_required(views.Enroll.as_view()), name="enroll"),
    
]