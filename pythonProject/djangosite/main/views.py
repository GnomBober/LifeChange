from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Module, Profile
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.forms import TextInput, PasswordInput
from django.http import JsonResponse
from .forms import CourseForm, ModuleForm, PaymentForm, SearchForm, RegistrationForm, CourseFilterForm
from django.urls import reverse
from django.db.models import Q

def mainpage(request):
    courses = Course.objects.prefetch_related('tags').all()
    return render(request, 'main/index.html', {'title': 'Курсы', 'courses': courses})

def profile_pg(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'main/profile_page.html', {'profile': profile})

def coursepg(request, id):
    course = get_object_or_404(Course, id=id)
    profile = Profile.objects.get(user=request.user) if request.user.is_authenticated else None

    # Проверка, есть ли курс в избранном
    is_favorite = profile.favorite_courses.filter(id=course.id).exists() if profile else False
    has_course = (
            profile.favorite_courses.filter(id=course.id).exists() or
            profile.current_courses.filter(id=course.id).exists() or
            profile.completed_courses.filter(id=course.id).exists()
    ) if profile else False

    if request.method == 'POST' and profile:
        if 'favorite' in request.POST:
            if is_favorite:
                # Удаление из избранного
                profile.favorite_courses.remove(course)
            else:
                # Добавление в избранное
                profile.favorite_courses.add(course)
            profile.save()
            return render(request, 'main/course.html', {'course': course})  # Перезагружаем страницу с обновленными данными

    return render(request, 'main/course.html', {
        'course': course,
        'is_favorite': is_favorite,
        'has_course': has_course
    })

def search_view(request):
    form = SearchForm(request.GET or None)
    query = None
    results = []

    if form.is_valid():
        query = form.cleaned_data['query']
        results = Course.objects.filter(
            title__icontains=query
        ) | Course.objects.filter(
            description__icontains=query
        ) | Course.objects.filter(
            tags__name__icontains=query
        )
        results = results.distinct()  # Убираем дубликаты

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
    if hasattr(request.user, 'profile') and request.user.profile.isTeacher:
        if request.method == 'POST':
            form = CourseForm(request.POST, request.FILES)
            if form.is_valid():
                course = form.save(commit=False)  # Создаем объект, но не сохраняем в базу
                course.save()  # Сохраняем объект
                form.save_m2m()  # Сохраняем связи ManyToMany

                # Добавляем курс в профиль пользователя
                request.user.profile.created_courses.add(course)
                request.user.profile.save()

                return redirect('catalog')  # Перенаправляем после успешного сохранения
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

from django.shortcuts import get_object_or_404, redirect
from .models import Course, Profile

def payment_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        # После успешной оплаты связываем курс с пользователем
        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            profile.current_courses.add(course)
            profile.save()
            return render(request, 'main/course.html', {'course': course})  # Перенаправляем обратно на страницу курса

    return render(request, 'main/payment.html', {'course': course})

def edit_course(request, id):
    profile = Profile.objects.get(user=request.user)
    course = get_object_or_404(Course, id=id)
    modules = Module.objects.filter(course=course, parent__isnull=True)  # Модули верхнего уровня

    if course not in profile.created_courses.all():
        return HttpResponseForbidden("Вы не можете редактировать этот курс, так как вы не являетесь его создателем.")

    # Обработка редактирования модуля
    module_id = request.GET.get('edit_module')  # Получаем ID модуля, который нужно редактировать
    module = None
    form = None

    if module_id:
        module = get_object_or_404(Module, id=module_id, course=course)
        form = ModuleForm(request.POST or None, instance=module)
        if form.is_valid():
            form.save()
            return redirect('edit_course', id=course.id)

    # Обработка добавления нового модуля
    if request.method == 'POST' and not module_id:  # Если не редактируем, а добавляем новый модуль
        parent_id = request.POST.get('parent_id')
        title = request.POST.get('title')
        content = request.POST.get('content')
        parent = Module.objects.get(id=parent_id) if parent_id else None

        # Создаем новый модуль
        Module.objects.create(course=course, parent=parent, title=title, content=content)
        return redirect('edit_course', id=course.id)

    return render(request, 'main/edit_course.html', {
        'course': course,
        'modules': modules,
        'form': form,
        'module': module,
    })

def course_progress(request, id):
    course = get_object_or_404(Course, id=id)
    modules = Module.objects.filter(course=course, parent=None).order_by('order')  # Верхнеуровневые модули
    return render(request, 'main/course_progress.html', {'course': course, 'modules': modules})

def module_detail(request, id):
    module = get_object_or_404(Module, id=id)
    submodules = Module.objects.filter(parent=module).order_by('order')  # Дочерние модули
    return render(request, 'main/module_detail.html', {'module': module, 'submodules': submodules})

def get_course_tree(course):
    """Функция для получения дерева модулей и подмодулей курса."""
    modules = Module.objects.filter(course=course, parent=None)
    tree = []
    for module in modules:
        tree.append({
            'module': module,
            'children': get_module_children(module)
        })
    return tree

def get_module_children(module):
    """Рекурсивная функция для получения дочерних элементов модуля."""
    children = module.children.all()
    return [{'module': child, 'children': get_module_children(child)} for child in children]

def course_catalog(request):
    courses = Course.objects.all()
    form = CourseFilterForm(request.GET or None)

    if form.is_valid():
        # Фильтрация по уровню сложности
        difficulty_levels = form.cleaned_data.get('difficulty_level')
        if difficulty_levels:
            if 'all' not in difficulty_levels:
                courses = courses.filter(difficulty_level__in=difficulty_levels)

        # Фильтрация по языку
        languages = form.cleaned_data.get('language')
        if languages:
            if 'any' not in languages:
                courses = courses.filter(language__in=languages)

        # Фильтрация по цене
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        if min_price is not None:
            courses = courses.filter(price__gte=min_price)
        if max_price is not None:
            courses = courses.filter(price__lte=max_price)

    return render(request, 'main/catalog.html', {'form': form, 'courses': courses})