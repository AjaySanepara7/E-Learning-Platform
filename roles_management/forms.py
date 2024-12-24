from django import forms
from django.contrib.auth.models import User
from roles_management.models import Profile, Enrollment


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"id": "password"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control border border-2 border-dark", "placeholder": "Username"})
        self.fields["first_name"].widget.attrs.update({"class": "form-control border border-2 border-dark", "placeholder": "First Name"})
        self.fields["last_name"].widget.attrs.update({"class": "form-control border border-2 border-dark", "placeholder": "Last Name"})
        self.fields["email"].widget.attrs.update({"class": "form-control border border-2 border-dark", "placeholder": "Email"})
        self.fields["password"].widget.attrs.update({"class": "form-control border border-2 border-dark", "placeholder": "Password"})
        self.fields["confirm_password"].widget.attrs.update({"class": "form-control border border-2 border-dark", "placeholder": "Confirm Password"})

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']


class ProfileForm(forms.ModelForm):
    person_gender = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Others")
    ]

    gender = forms.ChoiceField(
        widget = forms.RadioSelect,
        choices = person_gender
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={"class": "form-control border border-2 border-dark", "name": "date_of_birth", "type": "date"}) 
    )

    class Meta:
        model = Profile
        fields = ['gender', 'date_of_birth', 'profie_picture']


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['is_active']