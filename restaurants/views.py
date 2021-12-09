from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from django.db import IntegrityError
from django import forms
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
# from django.views.decorators.cache import never_cache
    # https://stackoverflow.com/questions/2095520/fighting-client-side-caching-in-django
from .models import User, Restaurant

import logging
import requests
import os 
import json
import environ
import base64


class SearchForm(forms.Form):
    city = forms.CharField(label="", 
                           widget=forms.TextInput(attrs={'placeholder': 'Name of city'}))


# For environment variable (for api key)
    # https://djangocentral.com/environment-variables-in-django/
env = environ.Env()
environ.Env.read_env()


# Get API key
# https://stackoverflow.com/questions/47949022/git-heroku-how-to-hide-my-secret-key
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Deployment#getting_your_website_ready_to_publish
api_key = env("API_KEY")


# Get an instance of a logger
logger = logging.getLogger(__name__)


def get_categories():
    # API call
    parameters = {                
        'key': api_key
    }
    
    response = requests.get('https://api.tomtom.com/search/2/poiCategories.json', params=parameters)    
    
    # Convert to JSON
    categories = response.json()['poiCategories']
    
    # Get restaurant category
    restaurant_category = None
    for category in categories:
        if category['name'] == 'Restaurant':
            restaurant_category = category
            break

    # Make a dictionary for the child categories
    child_categories = {}
    for childCategoryId in restaurant_category['childCategoryIds']:
       for category in categories:
           if category['id'] == childCategoryId:
               child_categories[category['id']] = category['name'] 
               break 

    return json.dumps(child_categories)


class SidebarForm(forms.Form):
    location = forms.CharField(label="Name of city", 
                           widget=forms.TextInput(attrs={'placeholder': 'Name of city'}))
    radius = forms.IntegerField(label="Radius", 
                           widget=forms.NumberInput(attrs={'placeholder': 'Radius'})) 
    
    categories_dictionary = json.loads(get_categories())
    # Converting categories_dictionary into list of tuples
        # https://www.geeksforgeeks.org/python-convert-dictionary-to-list-of-tuples/ 
    categories_choices = [(k, v) for k, v in categories_dictionary.items()] 
    
    categories = forms.MultipleChoiceField(label="Categories", choices = categories_choices,
                           widget=forms.SelectMultiple(attrs={'placeholder': 'Categories'}))    
        # https://stackoverflow.com/a/147793/

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
            return HttpResponseRedirect(reverse("results", args=[city]))
        else:
            # If the form is invalid, re-render the page with existing information.
            return render(request, "restaurants/index.html", {
                "form": form
            })
    
    return render(request, "restaurants/index.html", {
        "form": SearchForm()
    })


def geocode(city):      
    parameters = {
        'query': city,        
        'key': api_key
    }
    
    response = requests.get('https://api.tomtom.com/search/2/geocode/.json', params=parameters)
    
    lat_and_lon = response.json()['results'][0]['position']    
    return lat_and_lon


def search(lat_and_lon, radius, categories, offset):            
    parameters = {                
        'key': api_key,
        'lat': lat_and_lon['lat'],
        'lon': lat_and_lon['lon'],
        'radius': radius,
        'categorySet': categories, # this: '7315003,7315062' works
        'ofs': offset
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


def get_photo(photo_id):
    parameters = {                
        'key': api_key,
        'id': photo_id
    }

    response = requests.get('https://api.tomtom.com/search/2/poiPhoto', params=parameters)                
        
    encoded_string = base64.b64encode(response.content)        
   
    return encoded_string


# make this function smaller by breaking it into different parts (learned from App Academy Open (see Google Keep))
# @never_cache
def results(request, offset=0, city="None", radius=10000, categories='7315'):  
    try:
        # (Restaurant category number is 7315)                  
        if request.method == "POST":
            form = SidebarForm(request.POST)
            if form.is_valid():
                location = form.cleaned_data["location"]
                city = location
                radius = form.cleaned_data["radius"] 
                categories = form.cleaned_data["categories"]                         
                categories = ",".join(categories)

                return HttpResponseRedirect(reverse("results", 
                        args=[city, radius, categories])) 
            else:
                return render(request, "restaurants/results.html", {
                    "form": form
                })
            
        # Turn city name into coordinates
        lat_and_lon = geocode(city)

        # Search for nearby restaurants
        restaurants = search(lat_and_lon, radius, categories, offset)    

        if not restaurants:
            return render(request, "restaurants/results_no_match.html", {
                "city": city,                                             
                "form": SidebarForm(initial={'location': city, 'radius': radius})
            })

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
        restaurants_photos = []              
        for restaurant in restaurant_details:        
            if restaurant != 0 and 'photos' in restaurant['result']:
                photo_id = restaurant['result']['photos'][0]['id']
                encoded_string = get_photo(photo_id)  
                # https://stackoverflow.com/questions/41918836/how-do-i-get-rid-of-the-b-prefix-in-a-string-in-python
                restaurants_photos.append(encoded_string.decode('utf-8'))                  
            else:                    
            # if restaurant has no details and photos:                
                restaurants_photos.append(0)

        regular_ids_list = (request.user.saved_restaurants.values_list('regular_id', flat=True) 
                            if request.user.is_authenticated 
                            else [])  


        return render(request, "restaurants/results.html", {
            "city": city,  
            "radius": radius,
            "categories": categories,          
            "restaurants": restaurants,
            "restaurants_photos": restaurants_photos,    
            "regular_ids_list": regular_ids_list,          
            "form": SidebarForm(initial={'location': city, 'radius': radius}),
            'current_offset': offset
        })
    except:
        # Log an error message
        logger.error('Something went wrong!')  

        raise
            # https://www.reddit.com/r/Heroku/comments/muziyl/getting_server_error_500_on_django_heroku_website/gvc85yl?utm_source=share&utm_medium=web2x&context=3

# @never_cache
def add_or_remove(request, add_or_remove, regular_id, details_id):
    # if you have time, learn about the django get_or_create() method
        # (https://docs.djangoproject.com/en/3.1/ref/models/querysets/#get-or-create)        

    # Getting/creating a Restaurant object
    try:  
        restaurant = Restaurant.objects.get(regular_id=regular_id, details_id=details_id)
    except Restaurant.DoesNotExist:             
        restaurant = Restaurant.objects.create(regular_id=regular_id, details_id=details_id)
    
    # Adding the Restaurant object to the user's list
    if add_or_remove == "add":        
        request.user.saved_restaurants.add(restaurant) 
    else:
        request.user.saved_restaurants.remove(restaurant)     

    return HttpResponse("")
        # https://docs.djangoproject.com/en/3.1/topics/http/views/
        # ("Each view function is responsible for returning an HttpResponse object. (There are exceptions, but we’ll get to those later.)")        


# @never_cache
def restaurant_page(request, name, id, details_id):    
    # Make the following a single function to be shared with the profile function
    # (return an array with restaurant, restaurant_details, and photos_quantity)
    
    restaurant = get_restaurant(id)
    restaurant_details = get_restaurant_details(details_id) if details_id != '0' else 0
    
    if restaurant_details != 0 and 'photos' in restaurant_details['result']:
        restaurant_photos = get_restaurant_photos(restaurant_details['result']['photos'])
        # https://stackoverflow.com/questions/49284015/how-to-check-if-folder-is-empty-with-python
        # photos_quantity = len(os.listdir('restaurants/static/restaurants/Restaurant_Photos'))
        photos_quantity = len(restaurant_details['result']['photos'])
    else:
        restaurant_photos = []
        photos_quantity = 0

    regular_ids_list = (request.user.saved_restaurants.values_list('regular_id', flat=True) 
                        if request.user.is_authenticated 
                        else [])

    return render(request, "restaurants/restaurant.html", {
        "restaurant": restaurant['results'][0],
        "restaurant_details": restaurant_details,
        "restaurant_photos": restaurant_photos,
        "photos_quantity": photos_quantity,
        # https://stackoverflow.com/questions/48637178/do-django-templates-allow-for-range-in-for-loops
        "range": range(photos_quantity),
        "regular_ids_list": regular_ids_list
    })


def get_restaurant(id):
    parameters = {                        
        'entityId': id,
        'key': api_key
    }
    
    response = requests.get('https://api.tomtom.com/search/2/place.json', params=parameters)
    
    restaurant = response.json()
    return restaurant


def get_restaurant_photos(photo_ids):        
    restaurant_photos = []

    for photo_id in photo_ids:
        encoded_string = get_photo(photo_id['id'])
        restaurant_photos.append(encoded_string.decode('utf-8'))
    
    return restaurant_photos


# @never_cache
def profile(request, username):
    saved_restaurants_objects = request.user.saved_restaurants.all()
    saved_restaurants = []    
    
    restaurants_photos = []
    
    for saved_restaurant_object in saved_restaurants_objects:
        restaurant = get_restaurant(saved_restaurant_object.regular_id)
        restaurant = restaurant['results'][0]
        restaurant_details = get_restaurant_details(saved_restaurant_object.details_id) if saved_restaurant_object.details_id != '0' else 0

        saved_restaurants.append(restaurant)

        # Get photos   
        if restaurant_details != 0 and 'photos' in restaurant_details['result']:
            photo_id = restaurant_details['result']['photos'][0]['id']
            encoded_string = get_photo(photo_id) 
            restaurants_photos.append(encoded_string.decode('utf-8'))        
        else:                    
        # if restaurant has no details and photos:
            restaurants_photos.append(0)


    regular_ids_list = request.user.saved_restaurants.values_list('regular_id', flat=True)                           
    
    return render(request, "restaurants/profile.html", {
        "restaurants": saved_restaurants,
        "restaurants_photos": restaurants_photos,
        "regular_ids_list": regular_ids_list
    })


# Learned register, login, and logout functions from CS50W network project

def send_mail_to_me(username, email):
    send_mail(
        subject='New account on Trovare',
        message=f'Someone registered on https://trovare1.herokuapp.com/. \n Username: {username} \n Email: {email}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.EMAIL_HOST_USER]
    )
    return HttpResponse("")

def send_mail_to_user(username, email):
    send_mail(
        subject='Your new account on Trovare',
        message=f'Here is your account information on https://trovare1.herokuapp.com/. \n Username: {username} \n Email: {email}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )
    return HttpResponse("")    


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
        # Send email to me and new user
        send_mail_to_me(username, email)
        send_mail_to_user(username, email)
        
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