from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .extra_functions import snake_case, get_random_country, convert_to_underscore

# Create your views here.

def home(request):
    template = loader.get_template('home.html')
    context = { 
               "flag": "generated_flags/south_sudan.png",
               }
    
    return HttpResponse(template.render(context, request))

def marathon_mode(request):
    current_streak = 0 # if we havent loaded the page, streak = 0
    template = loader.get_template('marathon.html')
    
    next_country = get_random_country()
    flag_file_path = f"generated_flags/{next_country}.png"
    hints_on = request.POST.get("hints_on", "off")
    
    context = {
        "current_streak": current_streak,
        "correct_answer": next_country,
        "flag": flag_file_path,
        "hints_on" : hints_on,
        "hint": convert_to_underscore(next_country, 5 - int(next_country.count(" ")))
    }
    print(context['hint'])

    return HttpResponse(template.render(context, request))

def verify_answer(request): # this is the actual function that gets called and loads a new country endlessly
    streak = request.POST.get('current_streak', -1)
    guess = request.POST.get("guess", "").lower()
    correct_answer = request.POST.get("correct_answer", "").lower() 
    
    if guess.strip().lower() == correct_answer.strip().lower():
        next_country = get_random_country()
        flag_file_path = f"generated_flags/{next_country}.png"
        
        integer_likelihood = 5 - int(next_country.count(" "))

        template = loader.get_template('marathon.html')
        context={
            "current_streak": int(streak) + 1,
            "correct_answer": next_country,
            "flag": flag_file_path,
            "hint": convert_to_underscore(next_country, integer_likelihood)
        }
        print(context['hint'])
    else:
        template = loader.get_template('loser.html')
        context = {}
        
    return HttpResponse(template.render(context, request))

def loser(request):
    template = loader.get_template("loser.html")
    context = { }
    
    return HttpResponse(template.render(context, request))