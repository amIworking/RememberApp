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
        data = {"Error_message": "You didn't login"}
        return redirect('/login')
    elif len(User.objects.filter(username=cookies['username'])) == 0:
        data = {"Error_message": "This username doesn't exit"}
        return redirect('/login/registration')
    else:
        return cookies

def login_page(request):
    response = render(request, 'users/login/login.html')
    for key in request.COOKIES.keys():
        response.delete_cookie(key)
    return response


def registration(request):
    data = {'Error_message': ''}
    email = request.POST.get('email',False)
    username = request.POST.get('username',False)
    password = request.POST.get('password',False)
    reg = (email,username,password)
    if all(reg) == False:
        data ['Error_message'] = 'At least one field is empty'
    elif len(User.objects.filter(email = email))>0:
        data['Error_message'] = 'This email already exists'
    elif len(User.objects.filter(username = username))>0:
        data['Error_message'] = 'This nickname already exists'
    elif len(password) < 6 or len(password) > 30:
        data['Error_message'] = 'Your password has to be in a range between 6 and 30 ' \
                                'symbols'
    elif any(i.isdigit() for i in password) == False:
        data['Error_message'] = 'Your password has to contain at least 1 number'
    elif password.isdigit():
        data['Error_message'] = 'Your password has to contain at least 1 string'
    elif password.lower() == password or password.upper() == password:
        data['Error_message'] = 'Your password has to contain low and upper symbols'
    else:
        en_password = make_password(password)
        print(password)
        print(en_password)
        #print(check_password(password,en))
        new_user= User(email = email, username = username, password = en_password)
        new_user.save()
        return redirect('/login/')
    response = render(request, 'users/registration/registration.html', context=data)
    for key in request.COOKIES.keys():
        response.delete_cookie(key)
    return response

def setting_cookies(request, user):
    data = {'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name}
    test = redirect('/login/profile')
    req = render(request, 'users/profile/profile.html')
    for key, value in data.items():
        test.set_cookie(key, value, max_age=None)
    return test

def load_dict(list):
    target_list = []
    for i in list:
        local_dict = {}
        local_dict["name"] = i.name
        local_dict['lang_from'] = i.lang_from
        local_dict['lang_to'] = i.lang_to
        local_dict['count'] = len(Translates.objects.filter(dictionary=i))
        local_dict['level'] = i.level
        local_dict['raiting'] = 8.5
        target_list.append(local_dict)
    return target_list

def profile_page(request):
    cookies = check_verification(request)
    if False in cookies:
        return cookies[-1]
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





def login(request):
    login = request.POST.get('login',False)
    password = request.POST.get('password', False)
    reg = (login, password)
    data = {'Error_message': ''}
    if all(reg) == False:
        data['Error_message'] = 'At least one field is empty'
    username_check = User.objects.filter(username = login)
    email_check = User.objects.filter(email = login)
    if len(username_check):
        if check_password(password,username_check[0].password):
            return setting_cookies(request, username_check[0])
    elif len(email_check):
        if check_password(password, email_check[0].password):
            return setting_cookies(request, email_check[0])
    else:
        data['Error_message'] = "you wrote wrong username or password"
        return render(request, 'users/login/login.html', context=data)


