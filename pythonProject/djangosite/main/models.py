from django.db import models
from enum import Enum

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

    def __str__(self):
        return f"Курс {self.difficulty_level} на {self.language}"
