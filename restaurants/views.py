from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django import forms
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
    # https://stackoverflow.com/questions/2095520/fighting-client-side-caching-in-django
from .models import User

import requests
import urllib.parse

from shutil import copy
import os 
import glob

from datetime import date
import calendar


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


# Get API key
with open('/Users/azarnighian/Desktop/CS50W/Final Project/capstone/finalproject/finalproject/api_key.txt') as file:
    api_key = file.read().strip()


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


def geocode(city):
    # URL-encode city string
        # https://www.kite.com/python/answers/how-to-encode-a-url-in-python
        # https://www.urlencoder.io/python/#:~:text=In%20Python%203%2B%2C%20You%20can,uses%20UTF%2D8%20encoding%20scheme.
    # url_encoded_city = urllib.parse.quote(city)        
        
    parameters = {
        'query': city,        
        'key': api_key
    }
    
    response = requests.get('https://api.tomtom.com/search/2/geocode/.json', params=parameters)
    
    lat_and_lon = response.json()['results'][0]['position']    
    return lat_and_lon


def search(lat_and_lon):            
    parameters = {                
        'key': api_key,
        'lat': lat_and_lon['lat'],
        'lon': lat_and_lon['lon'],
        # 'radius':  ,
        'categorySet': 7315 #(Restaurant category number) 
    }
    
    response = requests.get('https://api.tomtom.com/search/2/nearbySearch/.json', params=parameters)
    
    restaurants = response.json()['results']
    return restaurants


def get_restaurant_details(id):
    parameters = {                
        'key': api_key,
        'id': id
    }
    
    response = requests.get('https://api.tomtom.com/search/2/poiDetails.json', params=parameters)
    
    restaurant_details = response.json()
    return restaurant_details


def get_photos(photo_id, counter, quantity):
        parameters = {                
            'key': api_key,
            'id': photo_id
        }
        
        response = requests.get('https://api.tomtom.com/search/2/poiPhoto', params=parameters)
        
        # https://www.w3schools.com/python/python_file_handling.asp
        if quantity == "one":
            f = open(f'/Users/azarnighian/Desktop/CS50W/Final Project/capstone/finalproject/restaurants/static/restaurants/Restaurants_Photos/Restaurant{counter}.jpg', 'wb')        
        else:
             f = open(f'/Users/azarnighian/Desktop/CS50W/Final Project/capstone/finalproject/restaurants/static/restaurants/Restaurant_Photos/Photo{counter}.jpg', 'wb')                   
        
        for chunk in response:
            if chunk:
                f.write(chunk)
        f.close()


# later, learn how to use csrf and not just use exempt 
# make this function smaller by breaking it into different parts
@csrf_exempt
@never_cache
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
    

    # Turn city name into coordinates
    lat_and_lon = geocode(city)

    # Search for nearby restaurants
    restaurants = search(lat_and_lon)    

    # Get the additional details for each restaurant
    restaurant_details = []
    for restaurant in restaurants:
        # If the restaurant has a details id
        if 'dataSources' in restaurant:
            id = restaurant['dataSources']['poiDetails'][0]['id']
            restaurant_details.append(get_restaurant_details(id))
        else:
            restaurant_details.append(0)

    # Get a photo for each restaurant
    
    delete_photos("results")
    
    counter = 1

    for restaurant in restaurant_details:        
        if restaurant != 0 and 'photos' in restaurant['result']:
            photo_id = restaurant['result']['photos'][0]['id']
            get_photos(photo_id, counter, "one")        
        # if restaurant has no details and photos:
        else:                    
            # https://stackoverflow.com/questions/123198/how-do-i-copy-a-file-in-python
            # https://thispointer.com/python-how-to-copy-files-from-one-location-to-another-using-shutil-copy/
            copy('restaurants/static/restaurants/no_image.png', 'restaurants/static/restaurants/Restaurants_Photos')

            # https://www.geeksforgeeks.org/python-os-rename-method/
            os.rename('restaurants/static/restaurants/Restaurants_Photos/no_image.png', f'restaurants/static/restaurants/Restaurants_Photos/Restaurant{counter}.jpg')

        counter += 1            
                
    return render(request, "restaurants/results.html", {
        "city": city,            
        "restaurants": restaurants,              
        "form": SidebarForm(initial={'location': city, 'radius': radius, 
                                    'keyword': keyword, 'min_price': min_price, 
                                    'max_price': max_price})
    })                                                        


@never_cache
def restaurant_page(request, name, id, details_id):    
    restaurant = get_restaurant(id)
    restaurant_details = get_restaurant_details(details_id) if details_id != '0' else 0
    
    delete_photos("restaurant_page")

    if restaurant_details != 0 and 'photos' in restaurant_details['result']:
        get_restaurant_photos(restaurant_details['result']['photos'])
        # https://stackoverflow.com/questions/49284015/how-to-check-if-folder-is-empty-with-python
        # photos_quantity = len(os.listdir('restaurants/static/restaurants/Restaurant_Photos'))
        photos_quantity = len(restaurant_details['result']['photos'])
    else:
        photos_quantity = 0

    # Changing each date in 'openingHours' to the name of the day of the week
        # Ex: '2019-02-05' should become 'Tuesday'
    # if 'openingHours' in restaurant['results'][0]:
    #     for time_range in restaurant['results'][0]['openingHours']['timeRanges']:
    #         # https://stackoverflow.com/questions/9847213/how-do-i-get-the-day-of-week-given-a-date
    #         this_date_string = time_range['startTime']['date']
    #         this_date = date.fromisoformat(this_date_string)
    #         this_date_name = calendar.day_name[this_date.weekday()]
            
    #         time_range['startTime']['date'] = this_date_name
    

    return render(request, "restaurants/restaurant.html", {
        "restaurant": restaurant['results'][0],
        "restaurant_details": restaurant_details,
        "photos_quantity": photos_quantity,
        # https://stackoverflow.com/questions/48637178/do-django-templates-allow-for-range-in-for-loops
        "range": range(photos_quantity)
    })


def get_restaurant(id):
    parameters = {                        
        'entityId': id,
        'key': api_key
    }
    
    response = requests.get('https://api.tomtom.com/search/2/place.json', params=parameters)
    
    restaurant = response.json()
    return restaurant


def delete_photos(type):
    # https://linuxize.com/post/python-delete-files-and-directories/
    if type == "results":
        files = glob.glob('/Users/azarnighian/Desktop/CS50W/Final Project/capstone/finalproject/restaurants/static/restaurants/Restaurants_Photos/*')
    else:
        files = glob.glob('/Users/azarnighian/Desktop/CS50W/Final Project/capstone/finalproject/restaurants/static/restaurants/Restaurant_Photos/*')
    
    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))


def get_restaurant_photos(photo_ids):
    counter = 0
    
    for photo_id in photo_ids:
        get_photos(photo_id['id'], counter, "all")
        counter += 1


@never_cache
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


def about(request):
    return render(request, "restaurants/about.html")