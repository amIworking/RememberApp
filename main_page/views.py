
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from  django.urls import reverse
from .models import *

# Create your views here.
pages = {"finding": 1, "creating":2}
def main_page(request):
    data = {"pages":pages}
    return render(request, "main_page/index.html", context=data)
def searh_page(request, search_try):
    if search_try == 'creating':
        return render(request, f"main_page/{search_try}/{search_try}.html")
    elif search_try == "finding":
        a = Dictionary.objects.all()
        all_lists = []
        for i in a:
            all_lists.append(i.name)
        data = {'all_lists': all_lists}
        return render(request, f"main_page/finding/finding.html",data)
    else:
        return HttpResponseNotFound("Opps")


#target.html
def open_list(request, search_try, path="main_page/finding/target_list.html"):
    searching = Dictionary.objects.filter(name = search_try)
    result = {}
    if len(searching) == 0:
        result = "This list don't exist"
    else:
        target_list = Translates.objects.filter(dictionary_id = searching[0].id)
        for i in target_list:
            result[i.word] = i.translate
    data = {'list_name':search_try, 'target_list':result}
    return data

def show_target_list(request, search_try):
    data = open_list(request, search_try)
    return render(request, "main_page/finding/target_list.html", data)

#searching
def list_searching(request):
    a = Dictionary.objects.all()
    all_lists = []
    for i in a:
        all_lists.append(i.name)
    answer = None
    if request.method == "POST":
        list_name = request.POST['searching']
        if list_name in all_lists:
            data = open_list(request, list_name)
            return render(request, "main_page/finding/target_list.html", data)
        else:
            answer = "we didn't find anything"
            data = {'all_lists':all_lists,'search_result' : answer}
            return render(request, f"main_page/finding/finding.html", context=data)


#Editing
def edit_target_list(request, search_try):
    data = open_list(request, search_try)
    return render(request, "main_page/editing/editing.html", data)


def update_saving(request, search_try):
    if request.method == "POST":

        # update dict name
        new_name = request.POST["list_name"]
        if search_try != new_name:
            old_name = Dictionary.objects.get(name=search_try)
            old_name.name = new_name
            old_name.save()

        # update values
        old_list = Translates.objects.filter(dictionary__name=search_try)
        old_dict = {i.word: (i.translate, i) for i in old_list}

        all_edited_data = [key for key in request.POST.keys() if key.startswith("word_")]

        updated = []
        for key, (value, translate) in old_dict.items():
            all_edited_data.remove(f"word_{key}")
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
            new_words.append(Translates(dictionary_id=old_name.id, word=word, translate=trans))

        Translates.objects.bulk_update(updated, fields=('word', 'translate'))
        Translates.objects.bulk_create(new_words)

        return redirect("/finding/")


def creating(request):
    translates = {}
    words = []
    trans = []
    if request.method == "POST":
        list_name = request.POST["list_name"]
        if list_name == "":
            data = {"Error_message":"You didn't fill the list name"}
            return render(request, "main_page/creating/creating.html", context=data)
        else:
            if request.POST["owner"] == 'private':
                new_list = Dictionary(name=list_name, lang_from="eng", lang_to="eng")
            else:
                new_list = Dictionary(name=list_name, lang_from = "eng", lang_to = "eng")
            new_list.save()
            new_id = Dictionary.objects.get(name=list_name)
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
    data = {"list_name":search_try}
    return render(request, "main_page/deleting/deleting.html", data)

def delete_list(request, search_try):
    all_names = []
    for i in Dictionary.objects.all():
        all_names.append(i.name)
    if search_try not in all_names:
        data = {"error_result":"This list dosen't exist", "color":"red"}
        return render(request, "main_page/finding/finding.html", data)
    else:
        target_list = Dictionary.objects.filter(name=search_try)
        target_words = Translates.objects.filter(dictionary_id=target_list[0].id)
        target_words.delete()
        target_list.delete()
        data = {"result": "Deleting has been made", "color":"green"}
        return render(request, "main_page/finding/finding.html", data)

def repeat_list(request, search_try):
    data = open_list(request, search_try)
    return render(request, 'main_page/repeating/repeating.html', context=data)




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