from django import forms
from django.contrib.auth.models import User
from roles_management.models import Profile, Enrollment
from course_app.models import Course
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"id": "password"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        email_check = User.objects.filter(email=email)
        if email_check.exists():
            raise forms.ValidationError('This Email already exists')
        if len(password) < 5:
            raise forms.ValidationError('Your password should have more than 5 characters')
        return super(UserForm, self).clean(*args, **kwargs)


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