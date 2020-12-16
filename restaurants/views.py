import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django import forms
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from django.views.decorators.csrf import csrf_exempt

from .models import User

class SearchForm(forms.Form):
    city = forms.CharField(label="", 
                           widget=forms.TextInput(attrs={'class': 'search_bar', 
                                                         'placeholder': 'Name of city'}))


class RegisterForm(forms.Form):
    username = forms.CharField(label="Username")
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    confirmation = forms.CharField(label="Confirm password", widget=forms.PasswordInput)


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


@csrf_exempt
def results(request):    
    data = json.loads(request.body)
    print(data)
    
    return render(request, "restaurants/results.html")        


@csrf_exempt
def testing(request):
    data = json.loads(request.body)
    print(data)
    
    # return render(request, "restaurants/results.html")
    return HttpResponseRedirect(reverse("results"))


def register(request):
    # Learned from CS50W network project

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "restaurants/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "restaurants/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:        
        return render(request, "restaurants/register.html", {
            "form": RegisterForm()
        })