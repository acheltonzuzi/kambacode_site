from django.contrib import admin
from .models import Course, Module, Lesson
from django.utils.html import format_html

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0
    fields = ('title', 'video_url')  # <-- removido 'order'
    ordering = ('order',)
    show_change_link = True


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0
    fields = ('title', 'description')  # <-- removido 'order'
    ordering = ('order',)
    show_change_link = True
    


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    
    list_display = ('thumbnail_preview','title', 'instructor', 'price','module_count','lesson_count','created_at', 'updated_at')
    search_fields = ('title', 'description', 'instructor__username')
    list_filter = ('created_at', 'instructor')
    ordering = ('title',)
    inlines = [ModuleInline]
    fieldsets = (
        ('Informações do Curso', {
            'fields': ('title','thumbnail', 'description', 'price')
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at','instructor', 'thumbnail_preview')
    
    # def save_model(self, request, obj, form, change):
    #     if not change or not obj.instructor_id:
    #         obj.instructor = request.user
    #     super().save_model(request, obj, form, change)
    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" width="80" height="60" style="object-fit:cover;border-radius:6px;" />', obj.thumbnail.url)
        return "—"
    thumbnail_preview.short_description = "Thumbnail"

    def save_model(self, request, obj, form, change):
        obj.save(request=request)
        
    def module_count(self, obj):
        return obj.modules.count()
    module_count.short_description = 'Modules'
    
    def lesson_count(self, obj):
    # Conta todas as aulas relacionadas aos módulos deste curso
        return Lesson.objects.filter(module__course=obj).count()
    lesson_count.short_description = 'Lessons'



@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'created_at', 'updated_at')
    list_filter = ('course',)
    search_fields = ('title', 'description')
    ordering = ('course', 'order')
    inlines = [LessonInline]
    fieldsets = (
        ('Informações do Módulo', {
            'fields': ('course', 'title', 'description')  # <-- removido 'order'
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'order', 'created_at', 'updated_at')
    list_filter = ('module',)
    search_fields = ('title',)
    ordering = ('module', 'order')
    fieldsets = (
        ('Informações da Aula', {
            'fields': ('module', 'title', 'video_url')  # <-- removido 'order'
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
