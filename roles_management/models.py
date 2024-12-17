from django.db import models
from django.contrib.auth.models import User
from phone_field import PhoneField
from django_countries.fields import CountryField
from django_extensions.db.models import TimeStampedModel


class Profile(TimeStampedModel):
    person_gender = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Others")
    ]

    countries = [
        ("I", "India")
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=100, choices=person_gender)
    date_of_birth = models.DateField()
    mobile = PhoneField(blank=True, help_text='Contact phone number', unique=True)
    country = CountryField()
    profie_picture = models.ImageField(upload_to='images/', null=True, blank=True)
    resume = models.FileField(upload_to='resume/', null=True, blank=True)


class Category(TimeStampedModel):
    category_id = models.CharField(max_length=300, primary_key=True)
    category_name = models.CharField(max_length=300)


class Course(TimeStampedModel):
    course_id = models.CharField(max_length=300, primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=300)
    start_date = models.DateField()
    end_date = models.DateField()
    prize = models.PositiveIntegerField()





