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

def list_searching(request):
    a = Dictionary.objects.all()
    all_lists = []
    for i in a:
        all_lists.append(i.name)
    answer = None
    if request.method == "POST":
        list_name = request.POST['searching']
        if list_name in all_lists:
            answer = "ok"
        else:
            answer = "we didn't find anything"
    data = {'all_lists':all_lists,'searh_result' : answer}
    return render(request, f"main_page/finding/finding.html", context=data)

def open_list(request, search_try):
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
    return render(request, f"main_page/finding/target_list.html", data)

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