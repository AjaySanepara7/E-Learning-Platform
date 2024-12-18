from django.db import models
from django_extensions.db.models import TimeStampedModel


class Category(TimeStampedModel):
    category_name = models.CharField(max_length=300)

    def __str__(self):
        return self.category_name


class Course(TimeStampedModel):
    course_id = models.CharField(max_length=300, primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=300)
    course_description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    course_image = models.ImageField(upload_to='course_image/', null=True, blank=True)

    def __str__(self):
        return self.course_name
