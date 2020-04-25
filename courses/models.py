import cloudinary.uploader
from django.db import models
from django.urls import reverse
from memberships.models import Membership

# Create your models here.

cloudinary.uploader.upload(open("vid.mp4", "rb"), resource_type="video")
cloudinary.uploader.upload(open("flo.jpg", "rb"), resource_type="image")


class Course(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=120)
    description = models.TextField()
    position = models.IntegerField(default=1)
    allowed_membership = models.ManyToManyField(Membership)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:detail', kwargs={'slug': self.slug})

    @property
    def lessons(self):
        return self.lesson_set.all().order_by('position')



class Lesson(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=120)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    content = models.TextField(blank=True, null=True)
    position = models.IntegerField()
    video = models.FileField(blank=True, null=True)
    thumbnail = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:lesson-detail', kwargs={
            'course_slug': self.course.slug,
            'lesson_slug': self.slug
        })

    @property
    def video_url(self):
        if self.video and hasattr(self.video, 'url'):
            return self.video.url
