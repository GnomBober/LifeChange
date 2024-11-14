from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainpage, name = 'home'),
    path('profile', views.profile, name = 'profile'),
    path('search/', views.search_view, name='search')
]