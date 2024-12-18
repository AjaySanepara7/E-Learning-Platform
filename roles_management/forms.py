from django import forms
from django.contrib.auth.models import User
from roles_management.models import Profile, Enrollment


class UserForm(forms.ModelForm):
    class Meta:
        model = User


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment