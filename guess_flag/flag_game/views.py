from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

def home(request):
    template = loader.get_template('home.html')
    context = { }
    
    return HttpResponse(template.render(context, request))