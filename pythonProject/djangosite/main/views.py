from django.shortcuts import render, redirect
from .models import Course
from .models import Profile
from .forms import SearchForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm
from django.contrib.auth import logout
from django.forms import TextInput, PasswordInput
from django.http import JsonResponse
from .forms import CourseForm
from .forms import PaymentForm

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
        results = Course.objects.filter(title__icontains=query) | Course.objects.filter(description__icontains=query) | Course.objects.filter(tags__name__icontains=query)

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


def filter_courses(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Пользователь не авторизован'}, status=400)

    profile = Profile.objects.get(user=request.user)

    # Получаем статус, переданный в запросе
    status = request.GET.get('status', '')

    if status == 'in_progress':
        courses = profile.current_courses.all()
    elif status == 'favorite':
        courses = profile.favorite_courses.all()
    elif status == 'completed':
        courses = profile.completed_courses.all()
    else:
        return JsonResponse({'error': 'Неизвестный статус'}, status=400)

    # Формируем данные для передачи в ответ
    course_data = []
    for course in courses:
        course_data.append({
            'id': course.id,
            'title': course.title,
            'photo': course.photo.url if course.photo else '',
        })

    return JsonResponse({'courses': course_data})

def teaching_page(request):
    # Проверяем, есть ли профиль и является ли пользователь учителем
    if hasattr(request.user, 'profile') and request.user.profile.isTeacher:
        if request.method == 'POST':
            form = CourseForm(request.POST, request.FILES)
            if form.is_valid():
                course = form.save(commit=False)
                course.save()
                form.save_m2m()  # Сохраняем связи для ManyToMany полей
                return redirect('catalog')  # Перенаправляем на каталог после успешного создания
        else:
            form = CourseForm()
        return render(request, 'main/teaching.html', {'form': form})
    else:
        return render(request, 'main/teaching.html', {'error_message': 'Войдите в аккаунт, являющийся учителем'})

def catalog(request):
    courses = Course.objects.all()

    # Получение параметров фильтров из GET-запроса
    difficulty_levels = request.GET.getlist('difficulty_level', [])
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    free = request.GET.get('free')
    languages = request.GET.getlist('language', [])

    # Применение фильтров
    if difficulty_levels:
        courses = courses.filter(difficulty_level__in=difficulty_levels)
    if min_price:
        courses = courses.filter(price__gte=min_price)
    if max_price:
        courses = courses.filter(price__lte=max_price)
    if free:
        courses = courses.filter(price=0)
    if languages:
        courses = courses.filter(language__in=languages)

    context = {
        'courses': courses,
        'selected_difficulty_levels': difficulty_levels,
        'min_price': min_price,
        'max_price': max_price,
        'free': free,
        'selected_languages': languages,
    }

    return render(request, 'main/catalog.html', context)

def payment_view(request):
    # Если пользователь отправил форму
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Тут можно добавить обработку данных формы, например, создание платежа
            # Например, если оплата прошла успешно, можно перенаправить на другую страницу
            return render(request, 'main/payment_success.html')  # Страница успешной оплаты
    else:
        # Если это GET-запрос, просто отображаем форму
        form = PaymentForm()

    return render(request, 'main/payment.html', {'form': form})