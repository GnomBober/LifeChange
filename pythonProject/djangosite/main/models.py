from random import choices
from django.db import models

class Object(models.Model):

    DIFFICULTY_LEVELS = [
        ('forbegin', 'Для Начинающих'),
        ('forinter', 'Для уверенных'),
        ('forpro', 'Для профессионалов'),
        ('forall', 'Для всех')
    ]

    LANGUAGES = [
        ('ru', 'Русский'),
        ('en', 'Английский'),
        ('any', 'Любой')
    ]

    TAGS = [
        ('c#', 'C#'),

    ]

    difficulty_level = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    language = models.CharField(max_length=50, choices=LANGUAGES)
    photo = models.ImageField(upload_to='photos/')
    description = models.TextField()
    tags = models.ManyToManyField('Tag', related_name='objects')
