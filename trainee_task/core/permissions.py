from typing import List

from rest_framework.permissions import BasePermission
from roles import Role


def create_user_permission(roles: List[Role]):
    class _PermissionClass(BasePermission):
        def has_permission(self, request, view):
            return request.user.is_authenticated and request.user.role in roles

    return _PermissionClass


IsStudent = create_user_permission([Role.STUDENT_ROLE])
IsTeacher = create_user_permission([Role.TEACHER_ROLE])
