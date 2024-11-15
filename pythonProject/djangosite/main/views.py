from django.shortcuts import render
from .models import Course
from django import forms
from .forms import SearchForm

def mainpage(request):
    return render(request, 'main/index.html')

def profile(request):
    return render(request, 'main/profile_page.html')

def course(request):
    return  render(request, 'main/course.html')

def search_view(request):
    form = SearchForm(request.GET or None)
    query = None
    results = []

    if form.is_valid():
        query = form.cleaned_data['query']
        results = Course.objects.filter(title__icontains=query) | Course.objects.filter(description__icontains=query)

    return render(request, 'main/search.html', {'form': form, 'query': query, 'results': results})