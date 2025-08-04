from flagpy import FlagIdentifier
import os, json

def snake_case(input_string):
    return input_string.lower().replace(" ", "_")

def get_flag_image(country_name):
    with open("valid_countries.json", "r") as file:
        valid_countries = json.load(file)
    if country_name not in valid_countries:
        flag_identifier = FlagIdentifier()
        flag_image = flag_identifier.get_flag_img(country_name)
        
        folder_path = os.path.join("images", "generated_flags")
        os.makedirs(folder_path, exist_ok=True)
        
        file_path = os.path.join(folder_path, snake_case(f"{country_name}.png"))
        flag_image.save(file_path)
        
        with open("valid_countries.json", "w") as file:
            json.dump(valid_countries, file, indent=4)

add_countries =  ["north korea", "south korea"]

for country in add_countries:
    get_flag_image(country)