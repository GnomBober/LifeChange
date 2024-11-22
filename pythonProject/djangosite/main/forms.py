from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, User
from django.forms import ModelForm, TextInput, PasswordInput


class SearchForm(forms.Form):
    query = forms.CharField(label='Поиск', max_length=100)


class RegistrationForm(UserCreationForm, ModelForm):
    # Дополнительные поля для регистрации
    name = forms.CharField(
        max_length=100,
        widget=TextInput(attrs={
            'class': 'name',
            'placeholder': 'Имя',
        }))
    age = forms.IntegerField(required=False)
    city = forms.CharField(max_length=100, required=False)
    photo = forms.ImageField(required=False)
    password1 = forms.CharField(
        widget=PasswordInput(attrs={
            'class': 'pass',
            'placeholder': 'Пароль',
        }),
        label="Password"
    )
    password2 = forms.CharField(
        widget=PasswordInput(attrs={
            'class': 'conf-pass',
            'placeholder': 'Подтвердите пароль',
        }),
        label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'name', 'age', 'city', 'photo']

        widgets = {
            "username": TextInput(attrs ={
                'class': 'username',
                'placeholder': 'Username',
            }),

        }



    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        # Создаем профиль для пользователя
        profile = Profile.objects.create(user=user,
                                         name=self.cleaned_data['name'],
                                         age=self.cleaned_data.get('age'),
                                         city=self.cleaned_data.get('city'),
                                         photo=self.cleaned_data.get('photo'))
        return user