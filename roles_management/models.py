from django.db import models
from django.contrib.auth.models import User
from course_app.models import Course
from django_countries.fields import CountryField
from django_extensions.db.models import TimeStampedModel


class Profile(TimeStampedModel):
    person_gender = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Others")
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=20, choices=person_gender)
    date_of_birth = models.DateField()
    mobile = models.CharField(max_length=25, unique=True)
    country = CountryField()
    profie_picture = models.ImageField(upload_to='images/', null=True, blank=True)
    resume = models.FileField(upload_to='resume/', null=True, blank=True)

    def __str__(self):
        return self.user.username


class Enrollment(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_active = models.BooleanField()

    def __str__(self):
        return f"student{self.profile} is enrolled in {self.course} course"

    class Meta:
        unique_together = ('user', 'course')