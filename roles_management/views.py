from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.conf import settings
from roles_management.models import Enrollment, Course
from roles_management.forms import UserForm, ProfileForm, EnrollmentForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import Permission
from django.contrib.auth import authenticate, login, logout
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from roles_management.tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages


User = get_user_model()

class Home(View):
    def get(self, request, *args, **kwargs):
        return render(request, "roles_management/home.html")
    

class SignupPage(View):
    user_form = UserForm()
    profile_form = ProfileForm()
    template_name = "roles_management/signup_page.html"

    def get(self, request, *args, **kwargs):
        user_form = UserForm()
        profile_form = ProfileForm()
        return render(request, self.template_name, {"user_form": user_form, "profile_form": profile_form})
    
    def post(self, request, *args, **kwargs):
        bound_user_form = UserForm(request.POST)
        bound_profile_form = ProfileForm(request.POST, request.FILES)
        if bound_user_form.is_valid() and bound_profile_form.is_valid():
            user_1 = bound_user_form.save()
            profile_1 = bound_profile_form.save(commit=False)
            profile_1.user = user_1
            profile_1.save()

            if profile_1.is_teacher == True:
                content_type = ContentType.objects.get_for_model(Course)
                course_permission = Permission.objects.get(content_type=content_type, codename="add_course")
                user_1.user_permissions.add(course_permission)
                user_1.save()
            return redirect(reverse("roles_management:login_page"))
        
        return render(request, self.template_name, {"user_form": self.user_form, "profil_form": self.profile_form })
    

class LoginPage(View):
    def get(self, request, *args, **kwargs):
        return render(request, "roles_management/login_page.html")
    
    def post(self, request, *args, **kwargs):
        user = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
        if user is not None:
            login(request, user)
            return redirect(reverse("roles_management:dashboard"))
        else:
            context={
                "login_failed": "Login failed. Invalid Credentials"
            }
            return render(request, "roles_management/login_page.html", context)
        

class Dashboard(View):
    def get(self, request, *args, **kwargs):
        return render(request, "roles_management/dashboard.html")
    
    