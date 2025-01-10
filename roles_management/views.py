
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.conf import settings
from course_app.models import Course, Category
from roles_management.models import Enrollment, Profile
from roles_management.forms import UserForm, ProfileForm, EnrollmentForm, ResetPasswordForm
from roles_management.tokens import account_activation_token, reset_password_token 
from django.shortcuts import render, redirect
from django.contrib.auth.models import Permission
from django.contrib.auth import authenticate, login, logout
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin


User = get_user_model()
    
class CourseView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "roles_management/course.html")
    

class PasswordResetConfirmView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "roles_management/password_reset_confirm.html")
    

class PasswordResetCompleteView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "roles_management/password_reset_complete.html")
    
    
class Signup(View):
    user_form = UserForm()
    profile_form = ProfileForm()
    template_name = "roles_management/signup.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("roles_management:dashboard"))
        user_form = UserForm()
        profile_form = ProfileForm()
        return render(request, self.template_name, {"user_form": user_form, "profile_form": profile_form})
    
    def post(self, request, *args, **kwargs):
        bound_user_form = UserForm(request.POST)
        bound_profile_form = ProfileForm(request.POST, request.FILES)
        if bound_user_form.is_valid() and bound_profile_form.is_valid():
            user_1 = bound_user_form.save(commit=False)
            user_1.set_password(bound_user_form.cleaned_data.get('password'))
            user_1.is_active = False
            user_1.save()
            profile_1 = bound_profile_form.save(commit=False)
            profile_1.user = user_1
            profile_1.save()

            if profile_1.is_teacher == True:
                content_type = ContentType.objects.get_for_model(Course)
                course_permission = Permission.objects.get(content_type=content_type, codename="add_course")
                user_1.user_permissions.add(course_permission)
                user_1.save()
            email = user_1.email
            return redirect(reverse("roles_management:verify-email")+ f"?email={email}")
        
        return render(request, self.template_name, {"user_form": self.user_form, "profil_form": self.profile_form })
    

class Login(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("roles_management:dashboard"))
        return render(request, "roles_management/login.html")
    
    def post(self, request, *args, **kwargs):
        user = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
        if user is not None:
            login(request, user)
            return redirect(reverse("roles_management:dashboard"))
        else:
            context={
                "login_failed": "Login failed. Invalid Credentials"
            }
            return render(request, "roles_management/login.html", context)
        

class Dashboard(View):
    def get(self, request, *args, **kwargs):
        enrollments = Enrollment.objects.filter(user=request.user)
        courses = [enrollment.course for enrollment in enrollments]
        teachers = Profile.objects.filter(is_teacher=True)
        is_enrolled = Enrollment.objects.filter()
        context = {
            "enrollments": enrollments,
            "courses": courses,
            "enrollment_count": len(enrollments),
            "course_count": len(Course.objects.all()),
            "category_count": len(Category.objects.all()),
            "teacher_count": len(teachers)
        }
        return render(request, "roles_management/dashboard.html", context)
    
    def post(self, request, *args, **kwargs):
        return redirect(reverse("roles_management:login"))
    
    
class Logout(View): 
    def get(self, request, *args, **kwargs):
        logout(request)
        context = {
                "logout": "Logout Successful"
            }
        return render(request, "roles_management/login.html", context)
    

class ProfileView(View):
    def get(self, request, *args, **kwargs):
        context = {
            "user": request.user,
            "profile": request.user.profile_set.first()
        }
        return render(request, "roles_management/profile.html", context)


class Enroll(View):
    def get(self, request, *args, **kwargs):
        course_id = kwargs.get("course_id")
        course = Course.objects.get(id=course_id)
        Enrollment.objects.create(user=request.user, course=course, is_active=True)
        context = {
            "course": course,
            "enrolled_successfully": "Enrolled Successfully"
        }
        return render(request, "course_app/course_detail.html", context)
    

class ResetPassword(View):
    def get(self, request, *args, **kwargs):
        return render(request, "roles_management/reset_password.html")
    
    def post(self, request, *args, **kwargs):
        current_site = get_current_site(request)
        user = request.user
        email = request.user.email
        subject = "Reset Password"
        message = render_to_string('roles_management/reset_password_message.html', {
            'request': request,
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': reset_password_token.make_token(user),
        })
        email = EmailMessage(
            subject, message, to=[email]
        )
        email.content_subtype = 'html'
        email.send()
        return redirect(reverse("roles_management:reset-password-done"))
    

class ResetPasswordDone(View):
    def get(self, request, *args, **kwargs):
        return render(request, "roles_management/reset_password_done.html")
    

class ResetPasswordConfirm(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and reset_password_token.check_token(user, token):
            context = {
                "validlink": True,
                "reset_password_form": ResetPasswordForm()
            }
            return render(request, "roles_management/reset_password_change.html", context)
        else:
            messages.warning(request, 'The link is invalid.')
        return render(request, 'roles_management/reset_password_confirm.html')
    

class ResetPasswordChange(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.check_password(request.POST.get("current_password")):
            if user.check_password(request.POST.get("new_password")):
                context = {
                "validlink": True,
                "reset_password_form": ResetPasswordForm(),
                "same_password": "The new password cannot be the same as the current password"
                }
                return render(request, "roles_management/reset_password_change.html", context)
            else:
                user.set_password(request.POST.get("new_password"))
                user.save()
                logout(request)
                context = {
                "success_change_password": "Password changed successfully"
                }
                return redirect(reverse("roles_management:reset-password-complete"))
        else:
            context = {
            "validlink": True,
            "reset_password_form": ResetPasswordForm(),
            "fail_change_password": "Invalid Password"
            }
            return render(request, "roles_management/reset_password_change.html", context)
        

class ResetPasswordComplete(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'roles_management/reset_password_complete.html')
       

class VerifyEmail(View):
    def get(self, request, *args, **kwargs):
        email = request.GET.get("email")
        user = User.objects.get(email=email)
        return render(request, "roles_management/verify_email.html", {"user": user})
    
    def post(self, request, *args, **kwargs):
        email = request.GET.get("email")
        user = User.objects.get(email=email)
        if user.is_active != True:
            current_site = get_current_site(request)
            email = email
            subject = "Verify Email"
            message = render_to_string('roles_management/verify_email_message.html', {
                'request': request,
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            email = EmailMessage(
                subject, message, to=[email]
            )
            email.content_subtype = 'html'
            email.send()
            return redirect(reverse("roles_management:verify-email-done"))
        else:
            return redirect(reverse("roles_management:signup"))
        

class VerifyEmailDone(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'roles_management/verify_email_done.html')
    

class VerifyEmailConfirm(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your email has been verified.')
            return redirect(reverse("roles_management:verify-email-complete"))
        else:
            messages.warning(request, 'The link is invalid.')
        return render(request, 'roles_management/verify_email_confirm.html')
    

class VerifyEmailComplete(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'roles_management/verify_email_complete.html')