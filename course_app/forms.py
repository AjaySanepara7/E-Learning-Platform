from django import forms
from course_app.models import Category, Course


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course