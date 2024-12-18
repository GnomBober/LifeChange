from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('course/<int:id>/', views.coursepg, name='course_detail'),
    path('', views.mainpage, name = 'home'),
    path('profile/', views.profile_pg, name = 'profile'),
    path('search/', views.search_view, name='search'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('catalog/', views.course_catalog, name='catalog'),
    path('filter_courses/', views.filter_courses, name='filter_courses'),
    path('teaching/', views.teaching_page, name='teaching'),
    path('course/<int:id>/edit/', views.edit_course, name='edit_course'),
    path('course/<int:id>/progress/', views.course_progress, name='course_progress'),
    path('course/module/<int:id>/', views.module_detail, name='module_detail'),
    path('payment/<int:course_id>/', views.payment_view, name='payment')
]