from django.db import models
from enum import Enum
from django.contrib.auth.models import User


class Tags(Enum):
    C_SHARP = 'C#'
    C_PLUS = 'C++'
    PYTHON = 'Python'
    JAVA = 'Java'
    HTML_CSS = 'HTML/CSS'
    DJANGO = 'Django'
    REACT = 'React'
    NODE = 'Node.js'
    FLASK = 'Flask'
    PANDAS = 'Pandas'
    FRONT = 'Frontend-разработка'
    BACK = 'Backend-разработка'
    JS = 'JavaScript'
    SQL = 'SQL'
    MACHINE = 'Машинное обучение'
    DATA = 'Анализ данных'
    MATH = 'Теория вероятностей и мат. статистика'
    ANDROID = 'Android'
    IOS = 'IOS'

class DifficultyLevel(Enum):
    FOR_BEGIN = 'Для начинающих'
    FOR_INTER = 'Для уверенных'
    FOR_PRO = 'Для профессионалов'
    FOR_ALL = 'Для всех'

class Languages(Enum):
    RU = 'Русский'
    EN = 'Английский'
    ANY = 'Любой'

# Модель для Tag
class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        choices=[(tag.name, tag.value) for tag in Tags]
    )

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=100)

    # Выбираем уровень сложности через CharField
    difficulty_level = models.CharField(
        max_length=20,
        choices=[(tag.name, tag.value) for tag in DifficultyLevel],
        default=DifficultyLevel.FOR_BEGIN.name
    )

    price = models.DecimalField(max_digits=10, decimal_places=2)
    language = models.CharField(
        max_length=20,
        choices=[(lang.name, lang.value) for lang in Languages],
        default=Languages.RU.name
    )

    photo = models.ImageField(upload_to='photos/')
    description = models.TextField()

    # Связь многие ко многим с моделью Tag
    tags = models.ManyToManyField(Tag, related_name='courses', blank=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")  # Связь с пользователем
    name = models.CharField(max_length=100)  # Имя пользователя
    age = models.PositiveIntegerField(null=True, blank=True)  # Возраст
    city = models.CharField(max_length=100, null=True, blank=True)  # Город
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)  # Фото профиля

    isTeacher = models.BooleanField(default=False, verbose_name="Является преподавателем")  # Флаг преподавателя

    # Связи с курсами
    completed_courses = models.ManyToManyField(Course, related_name="completed_by", blank=True)  # Пройденные курсы
    current_courses = models.ManyToManyField(Course, related_name="currently_taken_by", blank=True)  # Текущие курсы
    favorite_courses = models.ManyToManyField(Course, related_name="favorited_by", blank=True)  # Избранные курсы

    def __str__(self):
        return f"Профиль пользователя {self.user.username}"
