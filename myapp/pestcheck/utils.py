# pestcheck/utils.py
import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

# 1. Get coordinates using Map Maker Geocoding API
def get_coordinates(location_name):
    api_key = settings.GEOCODING_API_KEY
    url = "https://geocode.maps.co/search"
    params = {
        'q': location_name,
        'api_key': api_key,
        'format': 'json'
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            return lat, lon

    except requests.RequestException as e:
        logger.error(f"Geocoding error: {e}")

    return None, None
 

def get_pest_forecast(lat, lon, crop):
    api_key = settings.OPENWEATHER_API_KEY
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,
        'units': 'metric'
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        temp = data['main']['temp']
        humidity = data['main']['humidity']
        weather_desc = data['weather'][0]['description']

        # Pest risk logic
        if temp > 30 and humidity > 70:
            risk = "Very High"
        elif temp > 25 and humidity > 60:
            risk = "High"
        elif temp > 20 and humidity > 50:
            risk = "Moderate"
        else:
            risk = "Low"

        # Crop-specific recommendations
        crop = crop.lower()
        recommendation = ""

        if crop == "maize":
            if risk == "Very High":
                recommendation = "Inspect for armyworms and apply pesticide in the early morning. Watch for fall armyworm larvae."
            elif risk == "High":
                recommendation = "Check for leaf discoloration or damage regularly. Monitor for corn borers."
            elif risk == "Moderate":
                recommendation = "Ensure proper weeding and soil drainage. Scout for cutworms."
            else:
                recommendation = "Maintain standard field monitoring. Check for any signs of stalk rot."

        elif crop == "beans":
            if risk in ["High", "Very High"]:
                recommendation = "Watch for aphids and use neem-based insecticides if needed. Monitor for bean beetles."
            elif risk == "Moderate":
                recommendation = "Rotate crops to prevent soil-borne pests. Check for angular leaf spot."
            else:
                recommendation = "No major action needed, monitor weekly for any pest activity."

        elif crop == "sorghum":
            if risk in ["High", "Very High"]:
                recommendation = "Scout for stem borers and practice timely weeding. Watch for head bugs during flowering."
            elif risk == "Moderate":
                recommendation = "Use resistant varieties if available. Monitor for shoot fly."
            else:
                recommendation = "Monitor for pest outbreaks during flowering. Check for any signs of sooty mold."

        elif crop == "cassava":
            if risk == "Very High":
                recommendation = "Monitor for whiteflies and cassava mosaic virus symptoms. Check for green mites."
            elif risk == "High":
                recommendation = "Apply botanical pesticides and remove infected leaves. Watch for mealybugs."
            else:
                recommendation = "Promote airflow by spacing plants adequately. Monitor for bacterial blight."

        elif crop == "rice":
            if risk in ["High", "Very High"]:
                recommendation = "Check for rice blast and brown planthopper; drain flooded fields if needed. Watch for stem borers."
            elif risk == "Moderate":
                recommendation = "Maintain balanced fertilization and weed control. Monitor for leaf folder."
            else:
                recommendation = "Continue monitoring for any signs of fungal disease. Check for bacterial leaf blight."

        elif crop == "tomato":
            if risk == "Very High":
                recommendation = "Apply fungicides early to prevent blight, and stake plants to reduce moisture contact. Watch for whiteflies."
            elif risk == "High":
                recommendation = "Remove yellowing leaves and avoid overhead irrigation. Monitor for tomato hornworms."
            elif risk == "Moderate":
                recommendation = "Ensure good air circulation and scout for pests weekly. Check for early blight."
            else:
                recommendation = "Routine care should suffice in current conditions. Monitor for any aphid activity."

        elif crop == "wheat":
            if risk == "Very High":
                recommendation = "Inspect for rust diseases and apply fungicide if needed. Watch for aphids."
            elif risk == "High":
                recommendation = "Monitor for powdery mildew and septoria. Check for armyworm activity."
            elif risk == "Moderate":
                recommendation = "Ensure proper field sanitation. Watch for any signs of fusarium head blight."
            else:
                recommendation = "Standard monitoring practices recommended. Check for any leaf spot diseases."

        elif crop == "potato":
            if risk == "Very High":
                recommendation = "Monitor closely for late blight, apply preventive fungicides. Check for Colorado potato beetle."
            elif risk == "High":
                recommendation = "Remove infected plants immediately. Watch for leafhoppers and aphids."
            elif risk == "Moderate":
                recommendation = "Ensure proper hilling of plants. Monitor for early blight."
            else:
                recommendation = "Standard monitoring recommended. Check for any signs of viral diseases."

        elif crop == "soybean":
            if risk == "Very High":
                recommendation = "Scout for soybean aphids and apply treatment if threshold exceeded. Watch for white mold."
            elif risk == "High":
                recommendation = "Monitor for Japanese beetles and spider mites. Check for sudden death syndrome."
            elif risk == "Moderate":
                recommendation = "Ensure proper field rotation. Watch for bean leaf beetle."
            else:
                recommendation = "Routine scouting recommended. Check for any signs of bacterial pustule."

        elif crop == "cotton":
            if risk == "Very High":
                recommendation = "Monitor closely for bollworms and apply appropriate insecticides. Watch for aphid outbreaks."
            elif risk == "High":
                recommendation = "Check for whiteflies and spider mites. Remove heavily infested plants."
            elif risk == "Moderate":
                recommendation = "Implement biological control methods. Monitor for any signs of bacterial blight."
            else:
                recommendation = "Standard field monitoring recommended. Check for any early pest activity."

        else:
            recommendation = "No specific recommendation for this crop. Maintain general field monitoring practices."

        return {
            'temperature': temp,
            'humidity': humidity,
            'description': weather_desc,
            'risk': risk,
            'recommendation': recommendation
        }

    except requests.RequestException as e:
        logger.error(f"Weather API error: {e}")

    return None 