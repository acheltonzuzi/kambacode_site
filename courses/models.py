from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='courses/thumbnails/', null=True, blank=True)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Captura o request via kwargs (passado pelo admin, view ou signal)
        request = kwargs.pop('request', None)

        # Define o instrutor automaticamente, se não houver um ainda
        if not self.pk and not self.instructor_id and request is not None:
            self.instructor = request.user

        super().save(*args, **kwargs)
    
    @property
    def thumbnail_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        return '/static/img/placeholder.png'

    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            last = Module.objects.filter(course=self.course).aggregate(last_order=models.Max('order'))['last_order']
            self.order = 1 if last is None else last + 1
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class Lesson(models.Model):
    module = models.ForeignKey(Module, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    video_url = models.URLField()
    order = models.PositiveIntegerField(default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        if self.pk is None:
            last = Lesson.objects.filter(module=self.module).aggregate(last_order=models.Max('order'))['last_order']
            self.order = 1 if last is None else last + 1
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title