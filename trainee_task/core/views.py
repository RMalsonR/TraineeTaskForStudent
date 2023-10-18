from django.http import Http404
from django.db.models import Sum

from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response

from trainee_task.core.models import Lesson, LessonsView, ProductPermission, User
from trainee_task.core.permissions import IsStudent, IsTeacher
from trainee_task.core.serializers import LessonsListSerializer, LessonsRetrieveSerializer
from trainee_task.core.statuses import LessonsViewStatus, PermissionStatus
from trainee_task.core.roles import Role


class LessonsViewSet(viewsets.ReadOnlyModelViewSet):
    model = Lesson
    permission_classes = (IsStudent | IsTeacher)

    def get_qs_as_teacher(self):
        user_id = self.request.user.id
        qs = Lesson.objects.filter(products__owner=user_id).prefetch_related('products', 'views').all()

        return qs

    def get_qs_as_student(self):
        user_id = self.request.user.id
        qs = (Lesson.objects
              .filter(products__permissions=user_id,
                     views=user_id,
                     products__permissions__status=PermissionStatus.VALID.value)
              .prefetch_related('products', 'views').all())

        return qs

    def get_queryset(self):
        user = self.request.user

        if user.is_teacher:
            return self.get_qs_as_teacher()
        if user.is_student:
            return self.get_qs_as_student()

    def get_serializer_class(self):
        if self.action == 'list':
            return LessonsListSerializer
        return LessonsRetrieveSerializer

    def get_object_as_student(self):
        pk = self.kwargs['pk']
        user_id = self.request.user.id
        obj = (Lesson.objects
               .filter(products=pk,
                       products__permissions=user_id,
                       products__permissions__status=PermissionStatus.VALID.value,
                       views=user_id)
               .prefetch_related('products', 'views'))

        if not obj:
            raise Http404

        return obj

    def get_object_as_teacher(self):
        pk = self.kwargs['pk']
        user_id = self.request.user.id
        obj = Lesson.objects.filter(products=pk, products__owner=user_id).prefetch_related('products', 'views')

        if not obj:
            raise Http404

        return obj

    def get_object(self):
        user = self.request.user

        if user.is_teacher:
            return self.get_object_as_teacher()
        if user.is_student:
            return self.get_object_as_student()


class CountViewedLessons(APIView):
    permission_classes = IsAdminUser

    def get(self, request, format=None):
        cnt = LessonsView.objects.filter(status=LessonsViewStatus.SEEN.value).count()
        return Response({
            'count': cnt
        })


class CalculateViewedLessonsDuration(APIView):
    permission_classes = IsAdminUser

    def get(self, request, format=None):
        total_duration = LessonsView.objects.aggregate(Sum('duration'))
        return Response({
            'total_duration': total_duration
        })


class CountStudentOnProduct(APIView):
    permission_classes = IsAdminUser

    def get(self, request, format=None):
        pk = self.kwargs['pk']

        cnt = ProductPermission.objects.filter(product_id=pk, status=PermissionStatus.VALID.value).aggregate(Sum('user_id'))
        return Response({
            'students_count': cnt
        })


class CalculateProductsPurchases(APIView):
    permission_classes = IsAdminUser

    def get(self, request, format=None):
        pk = self.kwargs['pk']

        student_on_platform = User.objects.filter(role=Role.STUDENT_ROLE.value).count()
        students_on_product = (ProductPermission.objects
                               .filter(product_id=pk, status=PermissionStatus.VALID.value).aggregate(Sum('user_id')))

        if student_on_platform == 0:
            return Response({
                'purchase_percent': 0
            })

        result = (students_on_product / student_on_platform) * 100

        return Response({
            'purchase_percent': result
        })

