from flagpy import FlagIdentifier
import os

def snake_case(input_string):
    return input_string.lower().replace(" ", "_")

def get_flag_image(country_name):
    flag_identifier = FlagIdentifier()
    flag_image = flag_identifier.get_flag_img(country_name)
    
    folder_path = os.path.join("images", "generated_flags")
    os.makedirs(folder_path, exist_ok=True)
    
    file_path = os.path.join(folder_path, f"{country_name}.png")
    flag_image.save(file_path)
    
one_word_countries = [
    "afghanistan", "albania", "algeria", "andorra", "angola",
    "argentina", "armenia", "australia", "austria", "azerbaijan",
    "bahamas", "bahrain", "bangladesh", "barbados", "belarus",
    "belgium", "belize", "benin", "bhutan", "bolivia",
    "botswana", "brazil", "brunei", "bulgaria", "burundi",
    "cambodia", "cameroon", "canada", "chad", "chile",
    "china", "colombia", "comoros", "croatia", "cuba",
    "cyprus", "denmark", "djibouti", "dominica", "ecuador",
    "egypt", "eritrea", "estonia", "eswatini", "ethiopia",
    "fiji", "finland", "france", "gabon", "gambia",
    "georgia", "germany", "ghana", "greece", "grenada",
    "guatemala", "guinea", "guyana", "haiti", "honduras",
    "hungary", "iceland", "india", "indonesia", "iran",
    "iraq", "ireland", "israel", "italy", "jamaica",
    "japan", "jordan", "kazakhstan", "kenya", "kiribati",
    "kosovo", "kuwait", "kyrgyzstan", "laos", "latvia",
    "lebanon", "lesotho", "liberia", "libya", "liechtenstein",
    "lithuania", "luxembourg", "madagascar", "malawi", "malaysia",
    "maldives", "mali", "malta", "mauritania", "mauritius",
    "mexico", "micronesia", "moldova", "monaco", "mongolia",
    "montenegro", "morocco", "mozambique", "myanmar", "namibia",
    "nauru", "nepal", "netherlands", "nicaragua", "niger",
    "nigeria", "norway", "oman", "pakistan", "palau",
    "panama", "paraguay", "peru", "philippines", "poland",
    "portugal", "qatar", "romania", "russia", "rwanda",
    "samoa", "senegal", "serbia", "seychelles", "singapore",
    "slovakia", "slovenia", "somalia", "spain", "sudan",
    "suriname", "sweden", "switzerland", "syria", "tajikistan",
    "tanzania", "thailand", "togo", "tonga", "tunisia",
    "turkmenistan", "tuvalu", "uganda", "ukraine", "uruguay",
    "uzbekistan", "vanuatu", "venezuela", "vietnam", "yemen",
    "zambia", "zimbabwe"
]
for country in one_word_countries:
    try:
        get_flag_image(country)
    except KeyError:
        one_word_countries.remove(country)
        
print(one_word_countries)