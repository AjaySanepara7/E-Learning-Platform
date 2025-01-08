from django.shortcuts import render
from django.urls import reverse
from django.views import View
from course_app.models import Course, Category
from roles_management.models import Enrollment
from course_app.forms import CategoryForm, CourseForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404


class Courses(View):
    def get(self, request, *args, **kwargs):
        courses = Course.objects.all()
        context = {
             "courses": courses,
        }
        return render(request, "course_app/courses.html", context)
    

class EnrolledCourses(View):
    def get(self, request, *args, **kwargs):
        enrollments = Enrollment.objects.filter(user=request.user)
        context = {
             "courses": Course.objects.all(),
             "enrollments": enrollments
        }
        return render(request, "course_app/enrolled_courses.html", context)
    

class CourseDetail(View):
    def get(self, request, *args, **kwargs):
        course_id = kwargs.get("course_id")
        course = get_object_or_404(Course, id=course_id)
        enrollment_status = Enrollment.objects.filter(user=request.user, course=course).exists()
        context = {
            "course": course,
            "enrollment_status": enrollment_status
        }
        return render(request, "course_app/course_detail.html", context)


class CreateCourse(View):
    course_form_class = CourseForm
    template_name = "course_app/create_course.html"

    def get(self, request, *args, **kwargs):
        course_form = CourseForm()
        return render(request, self.template_name, {"course_form": course_form})
            
    def post(self, request, *args, **kwargs):
            course_form = CourseForm(request.POST, request.FILES)
            user = request.user
            if course_form.is_valid():
                if user.has_perm('course_app.add_course'):
                    course_form.save()
                    context = {
                        "course_created": "Course created successfully",
                        "courses": Course.objects.all()
                    }
                    return redirect(reverse("course_app:courses"))
                else:
                     return render(request, self.template_name, {"no_permission": "You don't have permission to create a course"})