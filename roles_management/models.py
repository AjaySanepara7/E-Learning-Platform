from django.db import models
from django.contrib.auth.models import User, AbstractUser
from course_app.models import Course
from django_countries.fields import CountryField
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

    
class Profile(TimeStampedModel):
    person_gender = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Others")
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email_is_verified = models.BooleanField(default=False)
    gender = models.CharField(max_length=20, choices=person_gender)
    date_of_birth = models.DateField()
    mobile = models.CharField(max_length=25, unique=True)
    country = CountryField()
    profie_picture = models.ImageField(upload_to='images/', null=True, blank=True)
    resume = models.FileField(upload_to='resume/', null=True, blank=True)
    is_teacher = models.BooleanField()

    def __str__(self):
        return self.user.username


class Enrollment(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_active = models.BooleanField()

    def __str__(self):
        return f"student{self.user.username} is enrolled in {self.course} course"

    class Meta:
        unique_together = ('user', 'course')


