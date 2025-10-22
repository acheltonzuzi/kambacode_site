from django.shortcuts import render
from .models import Course,Module
from django.views.generic import ListView
from django.views import View
from .forms.course_form import CourseForm
def home(request):
    courses=Course.objects.all()
    return render(request, 'home.html', {'courses': courses})

def course_detail(request, course_id:int):
    course = Course.objects.get(id=course_id)
    return render(request, 'couse_detail.html', {'course': course})

def course_lesson(request, course_id: int):
    course = Course.objects.get(id=course_id)
    modules = Module.objects.filter(course_id=course_id).prefetch_related('lessons')
    return render(request, 'course_lesson.html', {'course': course, 'modules': modules})

