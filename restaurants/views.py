from django import forms
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

class SearchForm(forms.Form):
    city = forms.CharField(label="City")


def index(request):
    # Check if method is POST
    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        form = SearchForm(request.POST)
        # Check if form data is valid (server-side)
        if form.is_valid():
            # Isolate the task from the 'cleaned' version of form data
            city = form.cleaned_data["city"]
            
            # Add the new task to our list of tasks
            # tasks.append(task)

            # Redirect user to list of tasks
            return HttpResponseRedirect(reverse("results", kwargs={'city': city}))
        else:
            # If the form is invalid, re-render the page with existing information.
            return render(request, "restaurants/index.html", {
                "form": form
            })
    
    return render(request, "restaurants/index.html", {
        "form": SearchForm()
    })


def results(request, city):
    return render(request, "restaurants/results.html", {
        "city": city
    })        