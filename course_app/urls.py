from django.urls import path
from course_app import views
from django.contrib.auth.decorators import login_required


app_name = "course_app"
urlpatterns = [
    path("courses", login_required(views.Courses.as_view()), name="courses"),
    path("create_course", views.CreateCourse.as_view(), name="create_course"),
    path("enrolled_courses", views.EnrolledCourses.as_view(), name="enrolled_courses"),
    path("course_detail/<int:course_id>", views.CourseDetail.as_view(), name="course_detail"),
]