from django import forms
from course_app.models import Category, Course


class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = ['category_name']


class CourseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"] = forms.ModelChoiceField(
                                        queryset=Category.objects.all(),
                                        widget = forms.Select(attrs={
                                            "class": "form-control border border-2 border-dark",
                                            "placeholder": "Category"}),
                                        empty_label = "Select a Category"
                                        )


    class Meta:
        model = Course
        fields = ['category', 'course_name', 'course_description', 'start_date', 'end_date', 'course_image']