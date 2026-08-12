import requests

# Remplacez par votre clé API (CalorieNinjas est gratuit et simple)
API_KEY = "VOTRE_CLE_API" 
API_URL = "https://api.calorieninjas.com/v1/nutrition?query="

def get_nutrition(query):
    header = {'X-Api-Key': API_KEY}
    response = requests.get(API_URL + query, headers=header)
    if response.status_code == 200:
        data = response.json()
        if data['items']:
            # On additionne si plusieurs aliments sont listés
            totals = {'calories': 0, 'protein_g': 0, 'carbohydrates_total_g': 0, 'fat_total_g': 0}
            for item in data['items']:
                for key in totals:
                    totals[key] += item[key]
            return totals
    return None

def calculate_bmr(weight, height, age, gender):
    if gender == "Homme":
        return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
