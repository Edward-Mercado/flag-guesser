import os, json
from flagpy import FlagIdentifier

def snake_case(input_string):
    return input_string.lower().replace(" ", "_")

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

done = False
while done == False:
    country = input("country ")
    if country == "done":
        done = True
        break
    get_flag_image(country)