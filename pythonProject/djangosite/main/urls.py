from django.urls import path
from . import views
from .forms import RegistrationForm

urlpatterns = [
    path('', views.mainpage, name = 'home'),
    path('profile/', views.profile, name = 'profile'),
    path('search/', views.search_view, name='search'),
    path('course/', views.course, name='course'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login')
]