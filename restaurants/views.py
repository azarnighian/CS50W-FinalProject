from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django import forms
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from django.views.decorators.csrf import csrf_exempt

from .models import User

import googlemaps

class SearchForm(forms.Form):
    city = forms.CharField(label="", 
                           widget=forms.TextInput(attrs={'placeholder': 'Name of city'}))


class RegisterForm(forms.Form):
    username = forms.CharField(label="Username")
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    confirmation = forms.CharField(label="Confirm password", widget=forms.PasswordInput)


class LogInForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


def index(request):    
# From CS50W notes
    # Check if method is POST
    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        form = SearchForm(request.POST)
        # Check if form data is valid (server-side)
        if form.is_valid():
            # Isolate the task from the 'cleaned' version of form data
            city = form.cleaned_data["city"]                                           
            
            # Redirect user
            return HttpResponseRedirect(reverse("results", kwargs={'city': city}))
        else:
            # If the form is invalid, re-render the page with existing information.
            return render(request, "restaurants/index.html", {
                "form": form
            })
    
    return render(request, "restaurants/index.html", {
        "form": SearchForm()
    })


# later, learn how to use csrf and not just use exempt 
@csrf_exempt
def results(request, city):
    results = search(city)            

    return render(request, "restaurants/results.html", {
        "city": city,
        "results": results
    })        


def search(city):
    # Get API key
    with open('/Users/azarnighian/Desktop/CS50W/Final Project/capstone/finalproject/finalproject/api_key.txt') as file:
        api_key = file.read().strip()

    # https://github.com/googlemaps/google-maps-services-python
    # https://www.youtube.com/watch?v=qkSmuquMueA
    
    gmaps = googlemaps.Client(key=api_key)
    
    # Geocode city 
    geocode_result = gmaps.geocode(city)
    lat_lng = geocode_result[0]["geometry"]["location"]
    lat = lat_lng["lat"]
    lng = lat_lng["lng"]    

    # Search for restaurants nearby city    
    places_result = gmaps.places_nearby(location=[lat,lng], radius=1000, type="restaurant")
    # return [places_result["results"], photos(gmaps, places_result["results"])]  
    return places_result["results"]


# def photos(gmaps, results):
#   photo_reference_string = results[0]["photos"][0]["photo_reference"]
#   photo = gmaps.places_photo(photo_reference_string, max_width=100)


def restaurant_details(request, name, id):
    with open('/Users/azarnighian/Desktop/CS50W/Final Project/capstone/finalproject/finalproject/api_key.txt') as file:
        api_key = file.read().strip()

    gmaps = googlemaps.Client(key=api_key)

    my_fields = ['formatted_address', 'name', 'formatted_phone_number', 'opening_hours', 'website']
    
    details_result = gmaps.place(place_id=id, fields=my_fields)
    
    return render(request, "restaurants/restaurant.html", {
        "details": details_result["result"]
    }) 


def profile(request, username):
    # this_user = User.objects.get(username=username)

    return render(request, "restaurants/profile.html")


# Learned register,login, and logout functions from CS50W network project

def register(request):    
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "restaurants/register.html", {
                "message": "Passwords must match.",
                "form": RegisterForm()
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "restaurants/register.html", {
                "message": "Username already taken.",
                "form": RegisterForm()
            })
        login(request, user)
        return HttpResponseRedirect(reverse("profile", args=[username]))
    else:        
        return render(request, "restaurants/register.html", {
            "form": RegisterForm()
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("profile", args=[username]))
        else:
            return render(request, "restaurants/login.html", {
                "message": "Invalid username and/or password.",
                "form": LogInForm()
            })
    else:
        return render(request, "restaurants/login.html", {
            "form": LogInForm()
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))        