import json
from django import forms
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from django.views.decorators.csrf import csrf_exempt

class SearchForm(forms.Form):
    city = forms.CharField(label="", 
                           widget=forms.TextInput(attrs={'class': 'search_bar', 
                                                         'placeholder': 'Name of city'}))


def index(request):
    return render(request, "restaurants/index.html")
    # with open('/Users/azarnighian/Desktop/CS50W/Final Project/capstone/finalproject/finalproject/api_key.txt') as f:
    #     api_key = f.read().strip()

    # # Check if method is POST
    # if request.method == "POST":
    #     # Take in the data the user submitted and save it as form
    #     form = SearchForm(request.POST)
    #     # Check if form data is valid (server-side)
    #     if form.is_valid():
    #         # Isolate the task from the 'cleaned' version of form data
    #         city = form.cleaned_data["city"]
            
    #         # Add the new task to our list of tasks
    #         # tasks.append(task)

    #         # Redirect user to list of tasks
    #         return HttpResponseRedirect(reverse("results", kwargs={'city': city}))
    #     else:
    #         # If the form is invalid, re-render the page with existing information.
    #         return render(request, "restaurants/index.html", {
    #             "form": form,
    #             "api_key": api_key
    #         })
    
    # return render(request, "restaurants/index.html", {
    #     "form": SearchForm(),
    #     "api_key": api_key
    # })

def results(request, city):
    data = json.loads(request.body)
    print(data)
    
    return render(request, "restaurants/results.html", {
        "city": city,
        "results": results
    })        

@csrf_exempt
def testing(request):
    data = json.loads(request.body)
    print(data)
    
    return render(request, "restaurants/results.html")