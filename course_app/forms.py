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
        self.fields["course_name"].widget.attrs.update({"class": "form-control border border-2 border-dark", "placeholder": "Course Name"})
        self.fields["course_description"].widget.attrs.update({"class": "form-control border border-2 border-dark", "placeholder": "Course Description"})
        self.fields["course_image"].widget.attrs.update({"class": "form-control border border-2 border-dark", "placeholder": "Course Image"})

    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            "class": "form-control border border-2 border-dark", 
            "name": "date_of_birth", 
            "type": "date"}) 
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={
            "class": "form-control border border-2 border-dark", 
            "name": "date_of_birth", 
            "type": "date"}) 
    )

    class Meta:
        model = Course
        fields = ['category', 'course_name', 'course_description', 'start_date', 'end_date', 'course_image']