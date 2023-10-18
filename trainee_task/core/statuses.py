from enum import Enum


class PermissionStatus(Enum):
    VALID = 'VALID'
    INVALID = 'INVALID'
    EXPIRED = 'EXPIRED'

    @classmethod
    def as_choices(cls):
        return (
            (cls.VALID.value, 'Доступ есть'),
            (cls.INVALID.value, 'Доступа нет'),
            (cls.EXPIRED.value, 'Доступ протух'),
        )


class LessonsViewStatus(Enum):
    SEEN = 'SEEN'
    NOT_SEEN = 'NOT_SEEN'

    @classmethod
    def as_choices(cls):
        return (
            (cls.SEEN.value, 'Просмотрено'),
            (cls.NOT_SEEN.value, 'Не просмотрено'),
        )
