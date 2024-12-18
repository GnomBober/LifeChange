# Generated by Django 5.1.3 on 2024-11-14 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_tag_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(choices=[('C_SHARP', 'C#'), ('C_PLUS', 'C++'), ('PYTHON', 'Python'), ('JAVA', 'Java'), ('HTML_CSS', 'HTML/CSS'), ('DJANGO', 'Django'), ('REACT', 'React'), ('NODE', 'Node.js'), ('FLASK', 'Flask'), ('PANDAS', 'Pandas'), ('FRONT', 'Frontend-разработка'), ('BACK', 'Backend-разработка'), ('JS', 'JavaScript'), ('SQL', 'SQL'), ('MACHINE', 'Машинное обучение'), ('DATA', 'Анализ данных'), ('MATH', 'Теория вероятностей и мат. статистика'), ('ANDROID', 'Android'), ('IOS', 'IOS')], max_length=50),
        ),
    ]
