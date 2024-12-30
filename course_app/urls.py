from django.urls import path
from course_app import views
from django.contrib.auth.decorators import login_required


app_name = "course_app"
urlpatterns = [
    path("create_course", views.CreateCourse.as_view(), name="create_course")
]