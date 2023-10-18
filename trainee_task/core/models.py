from django.contrib.auth.models import AbstractUser
from django.db import models

from trainee_task.core.roles import Role
from trainee_task.core.statuses import PermissionStatus, LessonsViewStatus


class User(AbstractUser):
    role = models.CharField(max_length=20, choices=Role.as_choices(),
                            default=Role.STUDENT_ROLE.value, verbose_name='Роль',
                            blank=False, null=False)

    @property
    def is_teacher(self):
        return self.role == Role.TEACHER_ROLE.value

    @property
    def is_student(self):
        return self.role == Role.STUDENT_ROLE.value


class Product(models.Model):
    title = models.CharField(max_length=254, verbose_name='Название продукта', blank=False, null=False)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Владелец продукта',
                              blank=False, null=False)
    permissions = models.ManyToManyField(User, through='ProductPermission', related_name='products')


class Lesson(models.Model):
    title = models.CharField(max_length=254, verbose_name='Название урока', blank=False, null=False)
    video_link = models.URLField(verbose_name='Ссылка на видео урока', blank=False, null=False)
    duration = models.PositiveIntegerField(verbose_name='Длительность урока (в секундах)', blank=False, null=False)
    products = models.ManyToManyField(Product, related_name='lessons')
    views = models.ManyToManyField(User, through='LessonsView', related_name='lessons')


class ProductPermission(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь с доступом', blank=False, null=False, related_name='products_permission')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт', blank=False, null=False, related_name='products_permission')
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False, verbose_name='Время создания записи')
    status = models.CharField(max_length=30, choices=PermissionStatus.as_choices(), verbose_name='Статус', blank=False, null=False)


class LessonsView(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', blank=False,
                                null=False, related_name='lessons_view')
    lesson_id = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Урок', blank=False, null=False, related_name='lessons_view')
    duration = models.PositiveIntegerField(verbose_name='Сколько пользователь посмотрел (в секундах)', blank=True, null=True)
    status = models.CharField(max_length=30, choices=LessonsViewStatus.as_choices(), verbose_name='Статус просмотра', blank=False,
                              null=False)
    updated_at = models.DateTimeField(auto_now_add=True, blank=False, null=False, verbose_name='Последняя дата просмотреа урока')
