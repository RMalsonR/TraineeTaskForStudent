from enum import Enum


class Role(Enum):
    TEACHER_ROLE = 'TEACHER_ROLE'
    STUDENT_ROLE = 'STUDENT_ROLE'

    @classmethod
    def as_choices(cls):
        return (
            (cls.TEACHER_ROLE.value, 'Преподаватель'),
            (cls.STUDENT_ROLE.value, 'Студент'),
        )
