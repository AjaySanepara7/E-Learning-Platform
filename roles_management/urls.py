from django.urls import path
from django.views.generic import RedirectView
from roles_management import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


app_name = "roles_management"
urlpatterns = [
    path("", views.Login.as_view(), name="login"),
    path("course", views.CourseView.as_view(), name="course"),
    path("signup", views.Signup.as_view(), name="signup"),    
    path("logout", views.Logout.as_view(), name="logout"),    
    path("dashboard", login_required(views.Dashboard.as_view()), name="dashboard"),    
    path("profile", login_required(views.ProfileView.as_view()), name="profile"),    
    path("enroll/<int:course_id>", login_required(views.Enroll.as_view()), name="enroll"),

    path("reset_password", login_required(views.ResetPassword.as_view()), name="reset_password"),    
    path("reset_password_done", login_required(views.ResetPasswordDone.as_view()), name="reset-password-done"),
    path('reset-password-confirm/<uidb64>/<token>/', login_required(views.ResetPasswordConfirm.as_view()), name='reset-password-confirm'),
    path("reset_password_change", login_required(views.ResetPasswordChange.as_view()), name="reset_password_change"),
    path('reset-password/complete/', views.ResetPasswordComplete.as_view(), name='reset-password-complete'),

    path('verify-email/', views.VerifyEmail.as_view(), name='verify-email'),
    path('verify-email/done/', views.VerifyEmailDone.as_view(), name='verify-email-done'),
    path('verify-email-confirm/<uidb64>/<token>/', views.VerifyEmailConfirm.as_view(), name='verify-email-confirm'),
    path('verify-email/complete/', views.VerifyEmailComplete.as_view(), name='verify-email-complete'),
     
]