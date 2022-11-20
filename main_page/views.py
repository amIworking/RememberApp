
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from  django.urls import reverse
from .models import *
from users.models import User
from users.views import load_dict

# Create your views here.
pages = {"finding": 1, "creating":2}

def check_verification(request):
    cookies = request.COOKIES
    login_check = ('username', "email")
    if any(i not in cookies.keys() for i in login_check):
        data = {"Error_message": "You didn't login"}
        return False, redirect('/login')
    elif len(User.objects.filter(username=cookies['username'])) == 0:
        data = {"Error_message": "This username doesn't exit"}

        return False,redirect('/login/registration')
    else:
        return cookies

def check_dict_owner(request,dict_name, owner_username):
    owner = User.objects.get(username = owner_username)
    if len(Dictionary.objects.filter(name=dict_name, owner=owner))==0:
        return False,redirect('/finding/')
    return []


def main_page(request):
    data = {"pages":pages}
    #return render(request, "main_page/main/index.html", context=data)
    return redirect('/finding')
def searh_page(request, search_try):
    if search_try == 'creating':
        cookies = check_verification(request)
        if False in cookies:
            return cookies[-1]
        return render(request, f"main_page/{search_try}/{search_try}.html")
    elif search_try == "finding":
        popular_dicts = load_dict(Dictionary.objects.filter(private=False))
        data = {'popular_dicts': popular_dicts}
        return render(request, f"main_page/finding/finding.html",data)
    else:
        return HttpResponseNotFound("Opps")


#target.html
def open_dict(request, search_try, path="main_page/finding/target_list.html"):
    searching = Dictionary.objects.filter(name = search_try)
    result = {}
    if len(searching) == 0:
        result = "This dictionary doesn't exist"
    else:
        target_list = Translates.objects.filter(dictionary_id = searching[0].id)
        for i in target_list:
            result[i.word] = i.translate
    owner = 'Public'
    if searching[0].owner!=None:
        owner = User.objects.get(id = searching[0].owner.id).username
    data = {'dict_name':search_try, 'target_dict':result, 'owner':owner}
    return data


def show_target_list(request, search_try):
    cookies = check_verification(request)
    if False in cookies:
        return cookies[-1]
    data = open_dict(request, search_try)
    data['own_dict'] = False
    data['followed'] = False
    target_dict = Dictionary.objects.filter(name = search_try)
    user_dists = User.objects.get(username=cookies.get('username')).added_dicts.all()
    if len(target_dict) == 0:
        return print("There is no dictionary like this")
    elif data['owner'] == cookies.get('username'):
        data['own_dict'] = True
    elif target_dict[0] in user_dists:
        data['followed'] = True
    data['lang_lvl'] = target_dict[0].level
    return render(request, "main_page/finding/target_list.html", data)

#searching
def list_searching(request):
    cookies = check_verification(request)
    if False in cookies:
        return cookies[-1]
    a = Dictionary.objects.filter(private=False)
    all_dicts = []
    for i in a:
        all_dicts.append(i.name)
    answer = None
    if request.method == "POST":
        dict_name = request.POST['searching']
        if all_dicts.count(dict_name)==1:
            data = open_dict(request, dict_name)
            return render(request, "main_page/finding/target_list.html", data)
        else:
            answer = "we didn't find anything"
            data = {'all_dicts':all_dicts,'search_result' : answer}
            return render(request, f"main_page/finding/finding.html", context=data)


#Editing
def edit_target_list(request, search_try):
    cookies = check_verification(request)
    if False in cookies:
        return cookies[-1]
    data = open_dict(request, search_try)
    check_result=check_dict_owner(request, search_try, cookies.get('username'))
    if False in check_result:
        return check_result[-1]
    return render(request, "main_page/editing/editing.html", data)


def update_saving(request, search_try):
    cookies = check_verification(request)
    if False in cookies:
        return cookies[-1]
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
    if False in cookies:
        return cookies[-1]
    if request.method == "POST":
        dict_name = request.POST["dict_name"]
        if dict_name == "":
            data = {"Error_message":"You didn't fill the dictionary name"}
            return render(request, "main_page/creating/creating.html", context=data)
        elif len(Dictionary.objects.filter(name=dict_name)):
            data = {"Error_message": "A dictionary with this name already exists"}
            return render(request, "main_page/creating/creating.html", context=data)
        else:
            user_id = User.objects.get(username=cookies['username'])
            private = False
            lang_from = request.POST.get('lang_from')
            lang_to = request.POST.get('lang_to')
            if lang_from=="" or lang_to == "":
                data = {"Error_message": "You didn't fill at least 1 language field"}
                return render(request, "main_page/creating/creating.html", context=data)
            if request.POST["owner"] == 'private':
                private = True
            new_list = Dictionary(name=dict_name, lang_from = lang_from, lang_to =
            lang_to, owner=user_id, private=private)
            new_list.save()
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
    if False in cookies:
        return cookies[-1]
    data = {"dict_name":search_try}
    return render(request, "main_page/deleting/deleting.html", data)

def delete_list(request, search_try):
    cookies = check_verification(request)
    if False in cookies:
        return cookies[-1]
    check_list = Dictionary.objects.filter(name = search_try)
    if len(check_list)==0:
        data = {"error_result":"This list dosen't exist", "color":"red"}
        return render(request, "main_page/finding/finding.html", data)
    elif Dictionary.objects.get(name = search_try).owner_id != User.objects.get(username=cookies.get('username')).id:
        data = {"error_result": "You can't delete list which does not belong to you",
                "color":
            "red"}
        return render(request, "main_page/finding/finding.html", data)
    else:
        owner_id = User.objects.get(cookies['username']).id
        target_list = Dictionary.objects.filter(name=search_try, owner_id = owner_id)
        target_words = Translates.objects.filter(dictionary_id=target_list[0].id)
        target_words.delete()
        target_list.delete()
        data = {"result": "Deleting has been made", "color":"green"}
        return redirect('finding/')

def adding_follow_dict(request, search_try):
    cookies = check_verification(request)
    if False in cookies:
        return cookies[-1]
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
    if False in cookies:
        return cookies[-1]
    target_dict = Dictionary.objects.filter(name=search_try)
    if len(target_dict) == 0:
        return print("There is no dictionary like this")
    user = User.objects.get(username=cookies.get('username'))
    if target_dict[0] not in user.added_dicts.all():
        return print("This dict is already unfollowed by you")
    user.added_dicts.remove(target_dict[0])
    user.save()
    return redirect(f'/finding/{search_try}/')




def repeat_list(request, search_try):
    cookies = check_verification(request)
    if False in cookies:
        return cookies[-1]
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



"""
pages = {"repeating": 1, "editor": 2, "deleting": 3, "creation":4}
def main_page(request):
    data = {"pages":pages}
    return render(request, "main_page/index.html", context=data)

def second_page(request):
    data = {"pages":second_pages}
    return render(request, "main_page/index.html", context=data)

def searh_page(request, search_try):
    search_try = search_try.lower()


    if searh_try not in pages:
        return HttpResponseNotFound("Opps")
    else:
        description = f"The answer: {pages[searh_try]}"
        data = {"description_result":description}
        return render(request, "main_page/test.html", context=data)
 

def redirect(request, searh_try):
    if searh_try in range(1,len(pages)+1):
        result = list(pages)[searh_try-1]
        return HttpResponseRedirect(f"/{result}/")

"""