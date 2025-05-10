# pestcheck/utils.py
import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

# pestcheck/utils.py
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

        if temp > 30 and humidity > 70:
            risk = "Very High"
        elif temp > 25 and humidity > 60:
            risk = "High"
        elif temp > 20 and humidity > 50:
            risk = "Moderate"
        else:
            risk = "Low"

        # Add recommendations
        recommendations = {
            'maize': "Watch for armyworms and maize stalk borers. Apply neem oil or appropriate pesticides.",
            'rice': "Risk of blast and bacterial leaf blight. Maintain field drainage and consider fungicide use.",
            'beans': "Monitor for aphids and rust. Use organic treatments like insecticidal soap.",
            'tomato': "High risk of late blight. Remove infected leaves and use copper-based sprays.",
            'wheat': "Watch for rust and aphids. Rotate crops and consider resistant varieties."
        }

        return {
            'temperature': temp,
            'humidity': humidity,
            'description': weather_desc,
            'risk': risk,
            'recommendation': recommendations.get(crop, "No specific recommendation.")
        }

    except requests.RequestException as e:
        logger.error(f"Weather API error: {e}")
        return None
