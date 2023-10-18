from django.urls import path, include
from rest_framework.routers import DefaultRouter

from trainee_task.core.views import (LessonsViewSet, CountViewedLessons,
                                     CalculateViewedLessonsDuration, CountStudentOnProduct,
                                     CalculateProductsPurchases)

router = DefaultRouter()
router.register('lessons', LessonsViewSet, basename='lessons')


urlpatterns = [
    path('', include(router.urls)),
    path('analytics/viewed_lessons/', CountViewedLessons.as_view(), name='viewed_lessons'),
    path('analytics/viewed_lessons_duration/', CalculateViewedLessonsDuration.as_view(), name='viewed_lessons_duration'),
    path('analytics/students_on_product/<int:pk>/', CountStudentOnProduct.as_view(), name='students_on_product'),
    path('analytics/product_purchases/<int:pk>/', CalculateProductsPurchases.as_view(), name='product_purchases'),
]