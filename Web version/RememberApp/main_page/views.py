import os
import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from  django.urls import reverse

# Create your views here.
list_path = "main_page/templates/main_page/lists"
lists = os.listdir(list_path)
pages = {"finding": 1, "creating":2}
def main_page(request):
    data = {"pages":pages}
    return render(request, "main_page/index.html", context=data)
def searh_page(request, search_try):
    if search_try in pages:
        data = {"amount_fields":range(5), "lists":lists}
        return render(request, f"main_page/{search_try}/{search_try}.html",data)
    elif search_try in lists:
        HttpResponseRedirect(f"/finding/")
        with open(f"{list_path+'/'+search_try}", "r") as r:
            result = json.loads(r.read())
        data = {"list_info":result, "list_name": search_try}
        return render(request, f"main_page/finding/showing.html",data)
    else:
        return HttpResponseNotFound("Opps")




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