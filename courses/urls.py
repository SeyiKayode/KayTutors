from django.urls import path
from .views import CourseList, CourseDetail, LessonDetail
app_name = 'courses'
urlpatterns = [
    path('', CourseList.as_view(), name='list'),
    path('<slug>/', CourseDetail.as_view(), name='detail'),
    path('<course_slug>/<lesson_slug>/', LessonDetail.as_view(), name='lesson-detail')
]