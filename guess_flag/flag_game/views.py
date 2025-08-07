from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .extra_functions import snake_case, get_random_country, convert_to_underscore, get_list_of_countries, get_background_color
from .extra_functions import convert_to_dictionary_list, get_accuracy_results, get_scrolling_country_flags, check_if_correct
# Create your views here.

def home(request):
    template = loader.get_template('home.html')
    context = {
        "flag_urls" : get_scrolling_country_flags(20),
        "flag_urls_2" : get_scrolling_country_flags(20),
    }
    
    return HttpResponse(template.render(context, request))

def marathon_mode(request):
    current_streak = 0 # if we havent loaded the page, streak = 0
    template = loader.get_template('marathon.html')
    
    next_country = get_random_country()
    flag_file_path = f"generated_flags/{snake_case(next_country)}.png"
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
    
    correct = check_if_correct((correct_answer, guess))
    
    if correct == True:
        next_country = get_random_country()
        flag_file_path = f"generated_flags/{snake_case(next_country)}.png"
        
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
        if hints_on == "on":
            hints_on_flavor_text = "were"
        else:
            hints_on_flavor_text = "were not"
            
        context = {
            "current_streak": int(streak),
            "guess" : guess,
            "guess_or_quit" : "You guessed",
            "flag" : f"generated_flags/{snake_case(correct_answer)}.png",
            "hints_on_flavor_text": hints_on_flavor_text,
            "correct_answer": correct_answer.title(),
        }
        
    return HttpResponse(template.render(context, request))

def loser(request):
    streak = request.POST.get('current_streak', -1)
    correct_answer = request.POST.get("correct_answer", "").lower() 
    hints_on = request.POST.get("hints_on", "off")
    if hints_on == "on":
        hints_on_flavor_text = "were"
    else:
        hints_on_flavor_text = "were not"
    
    template = loader.get_template("loser.html")
    context = { 
        "streak": streak,
        "correct_answer": correct_answer.title(),
        "guess_or_quit" : "You gave up",
        "hints_on_flavor_text": hints_on_flavor_text,
        "guess": None,
        "flag": f"generated_flags/{snake_case(correct_answer)}.png",
    }
    
    return HttpResponse(template.render(context, request))

def verify_answer_regular(request):
    unconverted_questions_list = request.POST.get("questions_list", "this is pretty bad guys")
    hints_on = request.POST.get("hints_on", "off")
    
    questions_list = convert_to_dictionary_list(unconverted_questions_list)
    number_of_questions = len(questions_list)
     
    correct_answers = []
    for i in range(number_of_questions):
        correct_answers.append(questions_list[i]['correct_answer'])    

    guesses = []
    for i in range(number_of_questions):
        i_plus_one = i+1
        guess = request.POST.get(f"guess_{i_plus_one}", "invalid_guess")
        guesses.append(guess)
        
    comparison_tuples = []
    for i in range(number_of_questions):
        comparison_tuples.append((correct_answers[i], guesses[i]))
    
    comparison_lists, percent_correct, number_correct, number_incorrect = get_accuracy_results(comparison_tuples)

    comparison_dictionaries = []
    for comparison_list in comparison_lists:
        comparison_dictionaries.append({
            "correct_answer" : comparison_list[0].title(),
            "flag_url": f"generated_flags/{snake_case(comparison_list[0])}.png",
            "guess" : comparison_list[1],
            "background_color" : get_background_color(comparison_list[2]),
            "result": comparison_list[2].upper(),
        })
        
    if hints_on == "on":
        were_hints_on = "were"
    else:
        were_hints_on = "were not"    
        
    context = {
        "question_results" : comparison_dictionaries,
        "number_correct" : number_correct,
        "number_incorrect" : number_incorrect,
        "percent_correct" : percent_correct,
        "were_hints_on" : were_hints_on,
    }
    template = loader.get_template("regular_game_answers.html")
    
    return HttpResponse(template.render(context, request))
    