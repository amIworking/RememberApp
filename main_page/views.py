
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from  django.urls import reverse
from django.views.generic import TemplateView

from .models import *
from users.models import User
from users.views import load_dict

# Create your views here.
pages = {"finding": 1, "creating":2}


class SomeView(TemplateView):
    template_name = "main_page/finding/finding.html"

    @login_required
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

def check_verification(request):
    cookies = request.COOKIES
    login_check = ('username', "email")
    if any(i not in cookies.keys() for i in login_check):
        return redirect('/login')
    elif len(User.objects.filter(username=cookies['username'])) == 0:
        return redirect('/login/registration')
    else:
        return cookies

def check_dict_owner(request,dict_name, owner_username):
    owner = User.objects.get(username = owner_username)
    return Dictionary.objects.filter(name=dict_name, owner=owner).exists()


def main_page(request):
    data = {"pages":pages}
    #return render(request, "main_page/main/index.html", context=data)
    return redirect('/finding')
def searh_page(request, search_try):
    if search_try == 'creating':
        cookies = check_verification(request)
        if type(cookies) != dict:
            return cookies
        return render(request, f"main_page/{search_try}/{search_try}.html")
    elif search_try == "finding":
        popular_dicts = load_dict(Dictionary.objects.filter(private=False))
        data = {'popular_dicts': popular_dicts}
        return render(request, f"main_page/finding/finding.html",data)
    else:
        return HttpResponseNotFound("Opps")


#target.html
def open_dict(search_try, reverse=False):
    dict = Dictionary.objects.filter(name__icontains=search_try)[0]
    if dict is None:
        return None
    return {
        'dict': dict,
        'target_dict': {
            i.word: i.translate
            for i in dict.translates_set.all()
        } if not reverse else {
            i.translate: i.word
            for i in dict.translates_set.all()
        },
        'owner': dict.owner and dict.owner.username or 'Public'
    }


def show_target_dict(request, search_try):
    cookies = check_verification(request)
    user = User.objects.get(username=cookies.get('username'))
    if type(cookies) != dict:
        return cookies
    data = open_dict(search_try)
    if data is None:
        return redirect("/finding/")
    data['own_dict'] = data['owner'] == cookies.get('username')
    data['followed'] = user.added_dicts.filter(id=data['dict'].id).exists()
    return render(request, "main_page/finding/target_dict.html", data)

#searching
def dicts_searching(request):
    cookies = check_verification(request)
    if type(cookies) != dict:
        return cookies
    all_dicts = Dictionary.objects.filter(private=False)

    if request.method == "POST":
        dict_name = request.POST['searching']
        if all_dicts.filter(name__icontains=dict_name).count() == 1:
            data = open_dict(dict_name)
            return render(request, "main_page/finding/target_dict.html", data)
        else:
            answer = "we didn't find anything"
            data = {'all_dicts': all_dicts, 'search_result' : answer}
            return render(request, f"main_page/finding/finding.html", context=data)


#Editing
def edit_target_dict(request, search_try):
    cookies = check_verification(request)
    if type(cookies) != dict:
        return cookies
    data = open_dict(search_try)
    if check_dict_owner(request, search_try, cookies.get('username')):
        return redirect('/finding/')
    return render(request, "main_page/editing/editing.html", data)


def update_saving(request, search_try):
    cookies = check_verification(request)
    if type(cookies) != dict:
        return cookies
    if request.method == "POST":
        # update dict name
        new_name = request.POST["dict_name"]
        old_dictionary = Dictionary.objects.get(name=search_try)
        if search_try != new_name:
            old_dictionary.name = new_name
            old_dictionary.save()
        """
        if request.POST('owner') == 'global':
            old_dictionary.owner_id = None
            old_dictionary.save()
        """
        # update values
        old_list = Translates.objects.filter(dictionary__name=search_try)
        old_dict = {i.word: (i.translate, i) for i in old_list}

        all_edited_data = [key for key in request.POST.keys() if key.startswith("word_")]

        updated = []
        for key, (value, translate) in old_dict.items():
            try:
                all_edited_data.remove(f"word_{key}")
            except ValueError:
                for i in old_list:
                    if i.word == key and i.translate == value:
                        Translates.objects.get(id=i.id).delete()
                continue
            new_key = request.POST[f"word_{key}"]
            new_value = request.POST[f"trans_{value}"]

            if value != new_value:
                translate.translate = new_value
            if new_key != key:
                translate.word = new_key

            if value != new_value or new_key != key:
                updated.append(translate)

        new_words = []
        for word in all_edited_data:
            key = word[5:]
            word = request.POST[f"word_{key}"]
            trans = request.POST[f"trans_{key}"]
            new_words.append(Translates(dictionary_id=old_dictionary.id, word=word,
                                        translate=trans))

        Translates.objects.bulk_update(updated, fields=('word', 'translate'))
        Translates.objects.bulk_create(new_words)

        return redirect("/finding/")


def creating(request):
    translates = {}
    words = []
    trans = []
    cookies = check_verification(request)
    if type(cookies) != dict:
        return cookies
    if request.method == "POST":
        dict_name = request.POST["dict_name"]
        if dict_name == "":
            data = {"Error_message":"You didn't fill the dictionary name"}
            return render(request, "main_page/creating/creating.html", context=data)
        elif len(Dictionary.objects.filter(name=dict_name)):
            data = {"Error_message": "A dictionary with this name already exists"}
            return render(request, "main_page/creating/creating.html", context=data)
        else:
            user_id = User.objects.get(username=cookies.get('username'))
            private = False
            lang_from = request.POST.get('lang_from')
            lang_to = request.POST.get('lang_to')
            if lang_from=="" or lang_to == "":
                data = {"Error_message": "You didn't fill at least 1 language field"}
                return render(request, "main_page/creating/creating.html", context=data)
            if request.POST["owner"] == 'private':
                private = True
            new_dict = Dictionary(name=dict_name, lang_from = lang_from, lang_to =
            lang_to, owner=user_id, private=private)
            new_dict.save()
            new_id = Dictionary.objects.get(name=dict_name)
            for key, value in request.POST.items():
                if value == "" and "word" in key or value == "" and "trans" in key:
                    data = {"Error_message": "You didn't fill at least 1 field"}
                    return render(request, "main_page/creating/creating.html", context=data)
                elif value != "" and "word" in key:
                    words.append(value)
                elif value != "" and "trans" in key:
                    trans.append(value)
            dictionary = dict(zip(words,trans))
            for key,value in dictionary.items():
                new_word = Translates(dictionary_id=new_id.id, word=key,
                                      translate=value)
                new_word.save()
            return redirect('/finding/')


def delete_confirming(request, search_try):
    cookies = check_verification(request)
    if type(cookies) != dict:
        return cookies
    data = {"dict_name":search_try}
    return render(request, "main_page/deleting/deleting.html", data)

def delete_dict(request, search_try):
    cookies = check_verification(request)
    if type(cookies) != dict:
        return cookies
    if len(Dictionary.objects.filter(name = search_try))==0:
        data = {"error_result":"This dictionary doesn't exist", "color":"red"}
        return render(request, "main_page/finding/finding.html", data)
    elif Dictionary.objects.get(name = search_try).owner_id != User.objects.get(username=cookies.get('username')).id:
        data = {"error_result": "You can't delete dictionary which does not belong to "
                                "you", "color":"red"}
        return render(request, "main_page/finding/finding.html", data)
    else:
        owner_id = User.objects.get(cookies['username']).id
        target_dict = Dictionary.objects.filter(name=search_try, owner_id = owner_id)
        target_words = Translates.objects.filter(dictionary_id=target_dict[0].id)
        target_words.delete()
        target_dict.delete()
        data = {"result": "Deleting has been made", "color":"green"}
        return redirect('finding/')

def adding_follow_dict(request, search_try):
    cookies = check_verification(request)
    if type(cookies) != dict:
        return cookies
    target_dict = Dictionary.objects.filter(name = search_try)
    if len(target_dict) == 0:
        return print("There is no dictionary like this")
    user = User.objects.get(username=cookies.get('username'))
    if target_dict[0] in user.added_dicts.all():
        return print("This dict is already followed by you")
    user.added_dicts.add(target_dict[0])
    user.save()
    return redirect(f'/finding/{search_try}/')

def remove_follow_dict(request, search_try):
    cookies = check_verification(request)
    if type(cookies) != dict:
        return cookies
    target_dict = Dictionary.objects.filter(name=search_try)
    if len(target_dict) == 0:
        return print("There is no dictionary like this")
    user = User.objects.get(username=cookies.get('username'))
    if target_dict[0] not in user.added_dicts.all():
        return print("This dict is already unfollowed by you")
    user.added_dicts.remove(target_dict[0])
    user.save()
    return redirect(f'/finding/{search_try}/')




def repeat_dict(request, search_try):
    cookies = check_verification(request)
    if type(cookies) != dict:
        return cookies
    get_dict = Dictionary.objects.filter(name = search_try)
    if len(get_dict) == 0:
        return print("This dict doesn't exist")
    word_list = Translates.objects.filter(dictionary = get_dict[0])
    if len(word_list)==0:
        return print("Your dict is empty")
    target_dict = {}
    for i in word_list:
        target_dict[f"{i.word}"]=f"{i.translate}"
    data = {"target_dict":target_dict, "dict_name": search_try}
    response = render(request, 'main_page/repeating/repeating.html', context=data)
    return response

def adding_points(request, search_try):
    return redirect(f'/finding/{search_try}/')
def speed_training(request):
    return render(request, 'main_page/speed/speed.html')

