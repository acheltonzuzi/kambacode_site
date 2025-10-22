from ninja import Router, Schema
from django.shortcuts import get_object_or_404
from .models import Course

router = Router(tags=["Courses"])

# Schema de resposta
class CourseSchema(Schema):
    id: int
    title: str
    description: str
    created_at: str
    thumbnail_url: str


# 🔹 Lista todos os cursos
@router.get("/courses", response=list[CourseSchema])
def list_courses(request):
    courses = Course.objects.all()
    data = []
    for course in courses:
        thumbnail_url = (
            request.build_absolute_uri(course.thumbnail.url)
            if course.thumbnail
            else request.build_absolute_uri("/static/img/placeholder.png")
        )
        data.append({
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "created_at": course.created_at.isoformat(),
            "thumbnail_url": thumbnail_url,
        })
    return data


# 🔹 Retorna curso por ID
@router.get("/courses/{course_id}", response=CourseSchema)
def get_course(request, course_id: int):
    course = get_object_or_404(Course, id=course_id)
    thumbnail_url = (
        request.build_absolute_uri(course.thumbnail.url)
        if course.thumbnail
        else request.build_absolute_uri("/static/img/placeholder.png")
    )
    return {
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "created_at": course.created_at.isoformat(),
        "thumbnail_url": thumbnail_url,
    }
