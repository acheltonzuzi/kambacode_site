from django.contrib import admin
from django.urls import path
from .views import home,course_detail,course_lesson

urlpatterns = [
    path('', home, name='home'),
    path('course/<int:course_id>/', course_detail, name='course_detail'),
    path('course/lesson/<int:course_id>/', course_lesson, name='course_lesson'),
]