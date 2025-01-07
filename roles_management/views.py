
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.conf import settings
from course_app.models import Course, Category
from roles_management.models import Enrollment, Profile
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
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.serializers import serialize
from django.core.serializers import deserialize
import json

User = get_user_model()

# class Home(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, "roles_management/home.html")
    
class CourseView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "roles_management/course.html")
    
class Dashboard2(View):
    def get(self, request, *args, **kwargs):
        return render(request, "roles_management/dashboard.html")
    

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
            user_1 = bound_user_form.save()
            profile_1 = bound_profile_form.save(commit=False)
            profile_1.user = user_1
            profile_1.save()

            if profile_1.is_teacher == True:
                content_type = ContentType.objects.get_for_model(Course)
                course_permission = Permission.objects.get(content_type=content_type, codename="add_course")
                user_1.user_permissions.add(course_permission)
                user_1.save()
            return redirect(reverse("roles_management:login"))
        
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
    context = {}
    def get(self, request, *args, **kwargs):
        return render(request, "roles_management/reset_password.html")
    
    def post(self, request, *args, **kwargs):
        recepient_id = request.POST.get("email")
        html_content = "<p>Click this link to <a href='http://127.0.0.1:8000/reset_password_confirm'> Reset <a> password.</p>"
        try:
            msg = EmailMultiAlternatives("reset password", "message", settings.EMAIL_HOST_USER, [recepient_id])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            self.context['result'] = 'Email sent successfully'
        except Exception as e:
            self.context['result'] = f'Error sending email: {e}'

        return render(request, "roles_management/reset_password.html", {"link": "Click the link sent to your registered email id to reset password"})


        

class VerifyEmail(View):
    def get(self, request, *args, **kwargs):
        return render(request, "roles_management/verify_email.html", {"user": request.user})
    
    def post(self, request, *args, **kwargs):
        if not request.user.email_is_verified:
            current_site = get_current_site(request)
            user = request.user
            email = request.user.email
            subject = "Verify Email"
            message = render_to_string('user/verify_email_message.html', {
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
            return redirect('verify-email-done')
        else:
            return redirect('signup')
        

class VerifyEmailDone(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'users/verify_email_done.html')
    

class VerifyEmailConfirm(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.email_is_verified = True
            user.save()
            messages.success(request, 'Your email has been verified.')
            return redirect('verify-email-complete')
        else:
            messages.warning(request, 'The link is invalid.')
        return render(request, 'user/verify_email_confirm.html')
    

class VerifyEmailComplete(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'user/verify_email_complete.html')
    




class SendMail(View):
    context = {}
    def get(self, request, *args, **kwargs):
        return render(request, "index.html", self.context)
    
    def post(self, request, *args, **kwargs):
        address = request.POST.get('address')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        html_content = "<p>This is an <strong>important</strong><a href='http://127.0.0.1:8000/login'> login <a> message.</p>"

        if address and subject and message:
            try:
                msg = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, [address])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                self.context['result'] = 'Email sent successfully'
            except Exception as e:
                self.context['result'] = f'Error sending email: {e}'
        else:
            self.context['result'] = 'All fields are required'

        return render(request, "index.html", self.context)
    

class ResetPasswordLink(View):
    def get(self, request, *args, **kwargs):
        return render(request, "roles_management/reset_password_confirm.html")
    
    def post(self, request, *args, **kwargs):
        user = request.user
        if not user.check_password(request.POST.get("password")):
            if request.POST.get("password") == request.POST.get("confirm_password"):
                user.set_password(request.POST.get("password"))
                user.save()
                context = {
                "success_change_password": "Password changed successfully"
                }
                return render(request, "roles_management/reset_password_confirm.html", context)
            else:
                context = {
                "match_password": "The confirm passwor did not match the password"
                }
                return render(request, "roles_management/reset_password_confirm.html", context)
        else:
            context = {
            "same_password": "The new password cannot be the same as the current password"
            }
            return render(request, "roles_management/reset_password_confirm.html", context)
