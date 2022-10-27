import os
import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from  django.urls import reverse
from .models import *

# Create your views here.
list_path = "main_page/templates/main_page/lists"
lists = os.listdir(list_path)
pages = {"finding": 1, "creating":2}
def main_page(request):
    data = {"pages":pages}
    return render(request, "main_page/index.html", context=data)
def searh_page(request, search_try):
    if search_try == 'creating':
        data = {"amount_fields":range(5), "lists":lists}
        return render(request, f"main_page/{search_try}/{search_try}.html",data)
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
    searching = Dictionary.objects.filter(name = search_try)\
        .values_list('id', flat=True)
    result = {}
    if len(searching) == 0:
        result = "This list don't exist"
    else:
        target_list = Translates.objects.filter(dictionary_id = searching[0])
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
        old_name = Dictionary.objects.get(name=search_try)
        old_list = Translates.objects.filter(dictionary_id = old_name.id)
        new_name = request.POST["list_name"]
        if search_try != new_name:
            old_name.name = new_name
            old_name.save()
        old_dict = {}
        for i in old_list:
            old_dict[i.word]=i.translate
        for key, value in old_dict.items():
            new_key = request.POST[f"word_{key}"]
            new_value = request.POST[f"trans_{value}"]
            if new_key != key:
                old_list.get(word=key).delete()
                new_word =Translates(dictionary_id = old_name.id, word=new_key,
                                    translate = new_value)
                new_word.save()
            else:
                if value != new_value:
                    old_list.filter(word = key).update(translate=new_value)
            data = open_list(request, new_name)
            data["Saving_Message"]="Saving was successful"
            return render(request, "main_page/finding/target_list.html", context=data)

def creating(request):
    if request.method == "POST":
        list_name = request.POST["list_name"]
        if list_name == "":
            data = {"Error_message":"You didn't fill the list name"}
            return render(request, "main_page/creating/creating.html", context=data)
        else:
            new_list = Dictionary(name=list_name, lang_from = "eng", lang_to = "eng")
            new_list.save()
            new_id = Dictionary.objects.get(name=new_list)
            for key, value in request.POST.items():
                if value == "" and "word" in key:
                    data = {"Error_message": "You didn't fill at least 1 field"}
                    return render(request, "main_page/creating/creating.html", context=data)
                else:
                    new_word = Translates(translate_id=new_id.id, word=key,
                                          translate=value)
                    new_word.save()
                    print("ok")






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