from django import forms
from django.contrib.auth.models import User
from roles_management.models import Profile, Enrollment
from course_app.models import Course


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"id": "password"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['mobile', 'gender', 'date_of_birth', 'profie_picture', 'country', 'resume', 'is_teacher']



class EnrollmentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["course"] = forms.ModelChoiceField(
            queryset=Course.objects.all(),
            widget = forms.Select(attrs={
                "class": "form-control border border-2 border-dark",
                "placeholder": "Course"}),
            empty_label = "Select a Course"
        )
        

    class Meta:
        model = Enrollment
        fields = ['course', 'is_active']