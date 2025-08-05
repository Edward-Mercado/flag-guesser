from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .extra_functions import snake_case, get_random_country, convert_to_underscore, get_list_of_countries, convert_to_dictionary_list

# Create your views here.

def home(request):
    template = loader.get_template('home.html')
    context = {
        "message": "welcome to flag guesser",
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
        "hint": convert_to_underscore(next_country, 3 + int(next_country.count(" ")))
    }

    return HttpResponse(template.render(context, request))

def regular_game_processing(request):
    successful = True
    try:
        number_of_questions = int(request.POST.get("number_of_questions", 0))
        if number_of_questions < 1:
            home(request)
            successful = False
        elif number_of_questions > 100:
            number_of_questions = 100
        
    except:
        successful = False
    
    if successful == True:
        
        hints_on = request.POST.get("hints_on", "off")

        template = loader.get_template("regular_game.html")
        context = {
            "number_of_questions": range(number_of_questions),
            "questions_list" : get_list_of_countries(number_of_questions),
            "hints_on": hints_on,
        }
        
        return HttpResponse(template.render(context, request))
    else:
        return redirect("/")

def verify_answer_marathon(request): # this is the actual function that gets called and loads a new country endlessly
    streak = request.POST.get('current_streak', -1)
    guess = request.POST.get("guess", "").lower()
    correct_answer = request.POST.get("correct_answer", "").lower() 
    hints_on = request.POST.get("hints_on", "off")
    
    if guess.strip().lower() == correct_answer.strip().lower():
        next_country = get_random_country()
        flag_file_path = f"generated_flags/{next_country}.png"
        
        integer_likelihood = 5 - int(next_country.count(" "))

        template = loader.get_template('marathon.html')
        context={
            "current_streak": int(streak) + 1,
            "correct_answer": next_country,
            "flag": flag_file_path,
            "hints_on": hints_on, 
            "hint": convert_to_underscore(next_country, integer_likelihood)
        }
        
    else:
        template = loader.get_template('loser.html')
        context = {}
        
    return HttpResponse(template.render(context, request))

def loser(request):
    template = loader.get_template("loser.html")
    context = { }
    
    return HttpResponse(template.render(context, request))

def verify_answer_regular(request):
    number_of_questions = request.POST.get("number_of_questions", 1)
    unconverted_questions_list = request.POST.get("questions_list", "this is pretty bad guys")
    correct_guess_count = 0
    correct_guesses = []
    incorrect_guess_count = 0
    incorrect_guesses = []
    
    questions_list = convert_to_dictionary_list(unconverted_questions_list)
    
    for i in range(number_of_questions):
        guess = request.POST.get(f"guess_{i}", "invalid_guess")
        print(unconverted_questions_list)
        if unconverted_questions_list[i] == guess.lower():
            correct_guess_count += 1
            correct_guesses.append(unconverted_questions_list[i])
        else:
            incorrect_guess_count += 1
            incorrect_guesses.append(unconverted_questions_list[i])
    
    return HttpResponse("placeholder")


    
    