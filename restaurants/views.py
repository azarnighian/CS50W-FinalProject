from django.shortcuts import render
from django.http import HttpResponse # DELETE AFTERWARDS

# Create your views here.
def index(request):
    return HttpResponse("Hello, world!")