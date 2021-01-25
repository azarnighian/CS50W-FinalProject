from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django import forms
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from django.views.decorators.csrf import csrf_exempt

from .models import User

import googlemaps

from shutil import copy
import os 

class SearchForm(forms.Form):
    city = forms.CharField(label="", 
                           widget=forms.TextInput(attrs={'placeholder': 'Name of city'}))


class SidebarForm(forms.Form):
    location = forms.CharField(label="Name of city", 
                           widget=forms.TextInput(attrs={'placeholder': 'Name of city'}))
    radius = forms.IntegerField(label="Radius from city", 
                           widget=forms.NumberInput(attrs={'placeholder': 'Radius'})) 
    keyword = forms.CharField(label="Keyword", 
                           widget=forms.TextInput(attrs={'placeholder': 'e.g. Vegan, Sandwich, Cafe'}))
    my_choices = ( 
        ("0", "0"), 
        ("1", "1"), 
        ("2", "2"), 
        ("3", "3"),
        ("4", "4"),          
    ) 
    min_price = forms.ChoiceField(label="Minimum price", choices = my_choices,
                           widget=forms.Select(attrs={'placeholder': 'Minimum Price'}))
    max_price = forms.ChoiceField(label="Maximum price", choices = my_choices,
                           widget=forms.Select(attrs={'placeholder': 'Maximum Price'}))


class RegisterForm(forms.Form):
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirmation = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))


class LogInForm(forms.Form):
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


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
            return HttpResponseRedirect(reverse("results", args=[city, "no", 1000, 'empty', 0, 4]))
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
def results(request, city, filters, radius, keyword, min_price, max_price):                   
    if request.method == "POST":
        form = SidebarForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data["location"]
            city = location
            radius = form.cleaned_data["radius"] 
            keyword = form.cleaned_data["keyword"] 
            min_price = form.cleaned_data["min_price"] 
            max_price = form.cleaned_data["max_price"]
            
            return HttpResponseRedirect(reverse("results", 
                    args=[city, "yes", radius, keyword, min_price, max_price]))                        
        else:
            return render(request, "restaurants/results.html", {
                "form": form
            })

    results = search(city, filters, radius, keyword, min_price, max_price)

    results_details = []
    for result in results:
        results_details.append(restaurant_details(result["place_id"]))

    # Get API key
    with open('/Users/azarnighian/Desktop/CS50W/Final Project/capstone/finalproject/finalproject/api_key.txt') as file:
        api_key = file.read().strip()

    if keyword == "empty":
        return render(request, "restaurants/results.html", {
            "city": city,             
            "restaurants": results_details,
            "api_key": api_key,
            "form": SidebarForm(initial={'location': city, 'radius': radius, 
                                        'min_price': min_price, 
                                        'max_price': max_price})                                                  
        })      
    else:
        return render(request, "restaurants/results.html", {
            "city": city,            
            "restaurants": results_details,
            "api_key": api_key,
            "form": SidebarForm(initial={'location': city, 'radius': radius, 
                                        'keyword': keyword, 'min_price': min_price, 
                                        'max_price': max_price})
        })                                                   


def search(city, filters, radius, keyword, min_price, max_price):
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

    if filters == "no":
        # Search for restaurants nearby city    
        places_result = gmaps.places_nearby(type="restaurant", 
                        location=[lat,lng], radius=radius)
    else:
        # Search for restaurants nearby city, with filters    
        places_result = gmaps.places_nearby(type="restaurant", location=[lat,lng], 
                        radius=radius, keyword=keyword, min_price=min_price,
                        max_price=max_price)                        

    # To save photos
    # get_photos(gmaps, places_result)

    return places_result["results"]


def get_photos(gmaps, result):        
    counter = 1

    for place in result['results']:
        if 'photos' in place:            
            photo_reference_string = place['photos'][0]['photo_reference']
            raw_image_data = gmaps.places_photo(photo_reference_string, max_width=300, max_height=300)        
            
            f = open(f'restaurants/static/restaurants/Restaurant_Images/Restaurant{counter}.jpg', 'wb')        
            for chunk in raw_image_data:
                if chunk:
                    f.write(chunk)
            f.close()

            counter += 1
        else:
            # https://stackoverflow.com/questions/123198/how-do-i-copy-a-file-in-python
            # https://thispointer.com/python-how-to-copy-files-from-one-location-to-another-using-shutil-copy/
            copy('restaurants/static/restaurants/unavailable-circle.png', 'restaurants/static/restaurants/Restaurant_Images')

            # https://www.geeksforgeeks.org/python-os-rename-method/
            os.rename('restaurants/static/restaurants/Restaurant_Images/unavailable-circle.png', f'restaurants/static/restaurants/Restaurant_Images/Restaurant{counter}.jpg')

            counter += 1


def restaurant_details(id):
    with open('/Users/azarnighian/Desktop/CS50W/Final Project/capstone/finalproject/finalproject/api_key.txt') as file:
        api_key = file.read().strip()

    gmaps = googlemaps.Client(key=api_key)

    my_fields = ['formatted_address', 'name', 'photo', 'place_id', 'formatted_phone_number', 'opening_hours', 'website']
    
    details_result = gmaps.place(place_id=id, fields=my_fields)

    return details_result["result"]

    # To get photos:
    # get_photos(gmaps, details_result)     


def restaurant_page(request, name, id):
    details = restaurant_details(id)

    return render(request, "restaurants/restaurant.html", {
        "details": details
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