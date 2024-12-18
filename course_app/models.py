import random
from django.db import models
from django_extensions.db.models import TimeStampedModel


class Category(TimeStampedModel):
    category_name = models.CharField(max_length=300, unique=True)


    def __str__(self):
        return self.category_name


class Course(TimeStampedModel):
    course_id = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=300)
    course_description = models.TextField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    course_image = models.ImageField(upload_to='course_image/', null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.course_id:
            prefix = self.course_name[:3]
            unique_number = random.randint(100, 999)
            self.course_id = prefix + unique_number

            super().save(*args, **kwargs)


    def __str__(self):
        return self.course_name