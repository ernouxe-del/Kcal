import requests

# Remplacez par vos identifiants Edamam
EDAMAM_APP_ID = 3c6dfc2f
EDAMAM_APP_KEY = 0b4ae419d3f79aa693c4439ac9d3dc02

def get_nutrition(query):
    """
    Analyse une phrase (ex: '100g chicken and 2 apples') 
    via l'API Edamam Nutrition Analysis.
    """
    url = "https://api.edamam.com/api/nutrition-data"
    
    params = {
        'app_id': EDAMAM_APP_ID,
        'app_key': EDAMAM_APP_KEY,
        'ingr': query
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            
            # Edamam renvoie 0 calories si l'aliment n'est pas reconnu
            if data.get('calories', 0) > 0:
                return {
                    'calories': data['calories'],
                    'protein_g': data['totalNutrients'].get('PROCNT', {}).get('quantity', 0),
                    'carbohydrates_total_g': data['totalNutrients'].get('CHOCDF', {}).get('quantity', 0),
                    'fat_total_g': data['totalNutrients'].get('FAT', {}).get('quantity', 0)
                }
        return None
    except Exception as e:
        print(f"Erreur API : {e}")
        return None

def calculate_bmr(weight, height, age, gender):
    # Formule de Harris-Benedict
    if gender == "Homme":
        return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
