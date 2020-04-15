from django.shortcuts import render, get_object_or_404
from .models import Course, Lesson
from memberships.models import UserMembership
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
class CourseList(ListView):
    model = Course
    template_name = 'courses/course_list.html'

class CourseDetail(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'courses/course_detail.html'

class LessonDetail(LoginRequiredMixin, View):
    def get(self, request, course_slug, lesson_slug, *args, **kwargs):
        course = get_object_or_404(Course, slug=course_slug)
        lesson = get_object_or_404(Lesson, slug=lesson_slug)
        user_membership = get_object_or_404(UserMembership, user=request.user)
        user_membership_type = user_membership.membership.membership_type
        course_allowed_mem_types = course.allowed_membership.all()
        context = {'object': None}
        if course_allowed_mem_types.filter(membership_type=user_membership_type).exists():
            context = {
                'object': lesson
            }
        return render(request, 'courses/lesson_detail.html', context)
