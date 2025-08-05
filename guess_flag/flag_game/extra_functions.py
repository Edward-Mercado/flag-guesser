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