from django.shortcuts import render, redirect
from .models import Course
from .models import Profile
from django import forms
from .forms import SearchForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm
from django.contrib.auth import logout
from django.forms import TextInput, PasswordInput

def mainpage(request):
    courses = Course.objects.prefetch_related('tags').all()
    return render(request, 'main/index.html', {'title': 'Курсы', 'courses': courses})

def profile_pg(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'main/profile_page.html', {'profile': profile})

def coursepg(request, id):  # Убедитесь, что аргумент id передается правильно
    try:
        course = Course.objects.get(id=id)  # Получаем курс по id
    except Course.DoesNotExist:
        return render(request, '404.html')  # Страница ошибки, если курс не найден
    return render(request, 'main/course.html', {'course': course})

def search_view(request):
    form = SearchForm(request.GET or None)
    query = None
    results = []

    if form.is_valid():
        query = form.cleaned_data['query']
        results = Course.objects.filter(title__icontains=query) | Course.objects.filter(description__icontains=query)

    return render(request, 'main/search.html', {'form': form, 'query': query, 'results': results})

# Регистрация пользователя
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Редирект на домашнюю страницу
    else:
        form = RegistrationForm()
    return render(request, 'main/register.html', {'form': form})

# Логин пользователя
# def user_login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('home')  # Редирект на домашнюю страницу
#     else:
#         form = AuthenticationForm()
#     return render(request, 'main/login.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
    else:
        form = AuthenticationForm()

    # Изменение атрибутов полей формы
    form.fields['username'].widget = TextInput(attrs={
        'class': 'username',
        'placeholder': 'Имя пользователя',
    })
    form.fields['password'].widget = PasswordInput(attrs={
        'class': 'pass',
        'placeholder': 'Пароль',
    })

    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('home')  # Редирект на домашнюю страницу

    return render(request, 'main/login.html', {'form': form})

# Выход пользователя
def user_logout(request):
    logout(request)
    return redirect('login')  # Редирект на страницу логина

def course_catalog(request):
    # Получаем все курсы из базы данных
    courses = Course.objects.all()
    return render(request, 'main/catalog.html', {'courses': courses})