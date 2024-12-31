from django.urls import path
from roles_management import views
from django.contrib.auth.decorators import login_required


app_name = "roles_management"
urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("login", views.LoginPage.as_view(), name="login_page"),    
    path("signup", views.SignupPage.as_view(), name="signup_page"),    
    path("dashboard", login_required(views.Dashboard.as_view()), name="dashboard"),    
    path("enroll", login_required(views.Enroll.as_view()), name="enroll"),
    path("reset_password", views.ResetPassword.as_view(), name="reset_password"),
    path('verify-email/', views.VerifyEmail.as_view(), name='verify-email'),
    path('verify-email/done/', views.VerifyEmailDone.as_view(), name='verify-email-done'),
    path('verify-email-confirm/<uidb64>/<token>/', views.VerifyEmailConfirm.as_view(), name='verify-email-confirm'),
    path('verify-email/complete/', views.VerifyEmailComplete.as_view(), name='verify-email-complete'),  
    path('sendmail/', views.SendMail.as_view(), name='sendmail'),  
    path('reset_password_confirm/', login_required(views.ResetPasswordLink.as_view()), name='reset_password_confirm'),  
]