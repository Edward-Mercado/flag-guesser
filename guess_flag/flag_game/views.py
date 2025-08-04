from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .extra_functions import snake_case, get_flag_emoji

# Create your views here.

def home(request):
    template = loader.get_template('home.html')
    context = { 
               "flag": get_flag_emoji("DE"),
               }
    
    return HttpResponse(template.render(context, request))

def marathon_mode(request):
    current_streak = request.GET.get('current_streak', -1) # if we havent loaded the page, streak = 0
    guess = request.POST.get('guess', 'this_is_invalid')
    
    if current_streak != -1:
        if snake_case(guess) == snake_case(str(request.GET.get('correct_answer'))):
            pass
        else:
            return HttpResponseRedirect('/loser')
    
    current_streak += 1
    
    template = loader.get_template('marathon.html')
    context = {
        "current_streak": current_streak,
        "correct_answer": "",
    }
    
def loser(request):
    template = loader.get_template("loser.html")
    context = {}
    return HttpResponse(template.render(context, request))