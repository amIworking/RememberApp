from typing import List

from django.contrib.auth.views import LoginView
from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from  django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password
from .models import *
from main_page.models import Dictionary, Translates
from  django.template import RequestContext

def check_verification(request):
    cookies = request.COOKIES
    login_check = ('username', "email")
    if any(i not in cookies.keys() for i in login_check):
        return redirect('/login')
    elif len(User.objects.filter(username=cookies['username'])) == 0:
        return redirect('/login/registration')
    else:
        return cookies

def login_page(request):
    response = render(request, 'users/login/login.html')
    request.COOKIES.clear()
    return response


class RegistrationForm(forms.Form):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True, min_length=4, max_length=20)
    password = forms.CharField(required=True, min_length=6, max_length=30)

    def clean_email(self):
        email = self.data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email already exists')
        return email

    def clean_username(self):
        username = self.data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username already exists')
        return username

    def clean_password(self):
        password = self.data['password']
        if any(i.isdigit() for i in password) == False:
            raise ValidationError('Your password has to contain at least 1 number')
        if password.isdigit():
            raise ValidationError('Your password has to contain at least 1 string')
        if password.lower() == password or password.upper() == password:
            raise ValidationError('Your password has to contain low and upper symbols')
        return make_password(password)

    def save(self):
        self.user = User(email=self.cleaned_data['email'],
                         username=self.cleaned_data['username'],
                         password=self.cleaned_data['password'])
        self.user.save()
        return self.user


def registration(request):
    form = RegistrationForm(request.POST)
    if form.is_valid():
        user = form.save()
        return redirect('/login/')
    return render(request, 'users/registration/registration.html', context={"form": form})

def setting_cookies(request, user):
    data = {'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name}
    response = redirect('/login/profile')
    #req = render(request, 'users/profile/profile.html')
    for key, value in data.items():
        response.set_cookie(key, value, max_age=None)
    return response

def load_dict(dicts: List[Dictionary]):
    return [
        {
            "name": i.name,
            'lang_from': i.lang_from,
            'lang_to': i.lang_to,
            'count': i.translates_set.count(),
            'level': i.level,
            'raiting': 8.5
        }
        for i in dicts
    ]

def profile_page(request):
    cookies = check_verification(request)
    if type(cookies) != dict:
        return cookies
    data = {'username':cookies['username'],
            'email':cookies['email'],
            'first_name':cookies['first_name'],
            "last_name":cookies['last_name']}
    user = User.objects.get(username = cookies.get('username'))
    own_dicts = load_dict(Dictionary.objects.filter(owner=user))
    data ['own_dicts'] = own_dicts
    followed_dicts = load_dict(user.added_dicts.all())
    data['followed_dicts'] = followed_dicts
    return render(request, 'users/profile/profile.html', context=data)


class LoginForm(forms.Form):
    login = forms.CharField(required=True, initial="")
    password = forms.CharField(required=True, initial="")

    def clean_login(self):
        login = self.data['login']
        self.user = User.objects.filter(username=login).first()
        if not self.user:
            self.user = User.objects.filter(email=login).first()
        if not self.user:
            raise ValidationError("you wrote wrong username or password")
        return login

    def clean_password(self):
        self.clean_login()
        password = self.data["password"]
        if not check_password(password, self.user.password):
            raise ValidationError("you wrote wrong username or password")
        return password


def login(request):
    if request.method == "GET":
        form = LoginForm()
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            return setting_cookies(request, form.user)
    return render(request, 'users/login/login.html', context={"form": form})
