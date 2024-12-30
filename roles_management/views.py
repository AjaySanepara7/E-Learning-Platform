from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.conf import settings
from roles_management.models import Enrollment, Course
from roles_management.forms import UserForm, ProfileForm, EnrollmentForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate, login, logout
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model


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
    
    def post(self, request, *args, **kwargs):
        logout(request)
        context = {
                "logout": "Logout Successful"
            }
        return render(request, "roles_management/login_page.html", context)
    

class Enroll(View):
    enroll_form = EnrollmentForm()

    def get(self, request, *args, **kwargs):
        enroll_form = EnrollmentForm()
        return render(request, "roles_management/enroll.html", {"enroll_form": enroll_form})
    
    def post(self, request, *args, **kwargs):
        enroll_form = EnrollmentForm(request.POST)
        user = request.user
        
        if enroll_form.is_valid():
            enrollment = enroll_form.save(commit=False)
            enrollment_object = Enrollment.objects.filter(user=user, course=enrollment.course)
            if enrollment_object:
                context = {
                    "already_enrolled": "User is already enrolled in this course select another course",
                    "enroll_form": EnrollmentForm()
                }
                return render(request, "roles_management/enroll.html", context)
            else:
                enrollment.user = user
                enrollment.is_active = True
                enrollment.save()
                return render(request, "roles_management/dashboard.html", {"enrolled_successfully": "Enrollment Successfull"})
        return render(request, "roles_management/enroll.html", {"enroll_form": EnrollmentForm()})
    

class ResetPassword(View):
    def get(self, request, *args, **kwargs):
        return render(request, "roles_management/reset_password.html")
    
    def post(self, request, *args, **kwargs):
        user = request.user
        if not user.check_password(request.POST.get("password")):
            if request.POST.get("password") == request.POST.get("confirm_password"):
                user.set_password(request.POST.get("password"))
                user.save()
                context = {
                "success_change_password": "Password changed successfully"
                }
                return render(request, "roles_management/reset_password.html", context)
            else:
                context = {
                "match_password": "The confirm passwor did not match the password"
                }
                return render(request, "roles_management/reset_password.html", context)
        else:
            context = {
            "same_password": "The new password cannot be the same as the current password"
            }
            return render(request, "roles_management/reset_password.html", context)