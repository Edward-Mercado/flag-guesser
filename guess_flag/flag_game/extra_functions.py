from flagpy import FlagIdentifier
import os, json, random

def snake_case(input_string):
    return input_string.lower().replace(" ", "_")

def convert_to_underscore(input_string, integer_likelihood): # converts strings to a bunch of underscores for hint
    list_of_characters = list(input_string)
    output_string = ""
    
    for character in list_of_characters:
        if character == " ":
            output_string += "   "
        else:
            if integer_likelihood > 0:
                if random.randint(1, integer_likelihood) == integer_likelihood:
                    output_string += character
                else:
                    output_string += "_ "
            else:
                output_string += "_ "
                
    return output_string

def get_flag_image(country_name):

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, "valid_countries.json")
    
    with open(file_path, "r") as file:
        valid_countries = list(json.load(file))
        
    flag_identifier = FlagIdentifier()
    flag_image = flag_identifier.get_flag_img(country_name)
        
    folder_path = os.path.join("images", "generated_flags")
    os.makedirs(folder_path, exist_ok=True)
        
    file_path = os.path.join(folder_path, snake_case(f"{country_name}.png"))
    flag_image.save(file_path)
        
    valid_countries.append(snake_case(country_name))
    with open("valid_countries.json", "w") as file:
        json.dump(valid_countries, file, indent=4)
        

def get_random_country():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, "valid_countries.json")
    
    with open(file_path, "r") as file:
        valid_countries = list(json.load(file))
        
    return random.choice(valid_countries)

def get_list_of_countries(number_of_questions):
    amount_remaining = number_of_questions # how many countries we need to get
    
    potential_flag_urls, potential_correct_answers, potential_hints = [], [], []
    flag_urls, correct_answers, hints = [], [], []
        
    done = False    
    while done == False:
        for i in range(amount_remaining):
            country_addition = get_random_country()
            potential_correct_answers.append(country_addition)
            potential_flag_urls.append(f"generated_flags/{snake_case(country_addition)}.png")
            potential_hints.append(convert_to_underscore(country_addition, 3 + int(country_addition.count(" "))))
                
        new_countries = 0        
                
        for item in potential_correct_answers:
            if item not in correct_answers:
                new_countries += 1
                correct_answers.append(item)
                flag_urls.append(potential_flag_urls[potential_correct_answers.index(item)])
                hints.append(potential_hints[potential_correct_answers.index(item)])
            
        amount_remaining -= new_countries 
        
        if amount_remaining <= 0:
            done = True
            if len(correct_answers) > number_of_questions:
                for i in range(number_of_questions):
                    correct_answers.remove(correct_answers[0])
                    flag_urls.remove(flag_urls[0])
                    hints.remove(hints[0])
                    
        potential_correct_answers.clear()
        potential_flag_urls.clear()
        potential_hints.clear()
            
    questions_list = []
    for i in range(number_of_questions):    
        questions_list.append({
            "correct_answer": correct_answers[i],
            "flag_url" : flag_urls[i],
            "hint": hints[i],
        })
        
    return questions_list

def convert_to_dictionary_list(unconverted_questions_list):
    split_keys = unconverted_questions_list.split(",")
    
    necessary_character_keys = []
    for list_word in split_keys:
        word = list(list_word)
        
        if word[3] == "c":
            for i in range(19):
                word.remove(word[0])    
        elif word[3] == "l":
            for i in range(12):
                word.remove(word[0])
        elif word[3] == "i":
            for i in range(8):
                word.remove(word[0])
                
        for character in word:
            if character in ["[", "]", "{", "}", "'"]:
                word.remove(character)
                
        if split_keys.index(list_word) % 3 == 2:
            word.remove(word[len(word) - 1])    
                
        word.remove(word[0])
        
        cleared_word_string = ""
        for character in word:
            cleared_word_string += character
        
        necessary_character_keys.append(cleared_word_string)     
                
    number_of_dictionaries = int(len(necessary_character_keys) / 3)
    
    list_of_dictionaries = []
    for i in range(number_of_dictionaries):
        true_index = 3 * i
        list_of_dictionaries.append(
            {
                "correct_answer" : necessary_character_keys[true_index],
                "flag_url" : necessary_character_keys[true_index + 1],
                "hint" : necessary_character_keys[true_index + 2],
            }
        )
        
    return list_of_dictionaries
    
convert_to_dictionary_list(
    str([{'correct_answer': 'senegal', 'flag_url': 'generated_flags/senegal.png', 'hint': '_ _ _ e_ al'}, 
    {'correct_answer': 'lithuania', 'flag_url': 'generated_flags/lithuania.png', 'hint': '_ _ t_ _ _ n_ _ '}, 
    {'correct_answer': 'canada', 'flag_url': 'generated_flags/canada.png', 'hint': 'ca_ ada'}])
)