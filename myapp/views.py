import datetime
import requests
from django.shortcuts import render

# Create your views here.
def index(request):
    API_KEY = open("C:\\Users\\DELL\\Weather-app\\API_KEY", "r").read()
    current_weather_url ="https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forecast_url ="https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=currently,minutely,hourly,alerts&appid={}"

    if request.method == "POST":
        first_city = request.POST['first_city']
        second_city = request.POST.get('second_list', None)

        weather_data1, daily_forecasts1 = weather_and_forecast(first_city, API_KEY, current_weather_url, forecast_url)

        if second_city:
            weather_data2, daily_forecasts2 = weather_and_forecast(second_city, API_KEY, current_weather_url, forecast_url)
        else:
            weather_data2, daily_forecasts2 = None, None

        context = {
            "weather_data1" : weather_data1,
            "daily_forecasts1" : daily_forecasts1,
            "weather_data2" : weather_data2,
            "daily_forecasts2" : daily_forecasts2,

        }
        return render(request, "myapp/index.html", context)
    else:
        return render(request, "myapp/index.html")


def weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    # Get current weather data
    response = requests.get(current_weather_url.format(city, api_key)).json()
    print("Current Weather Response:", response)

    # Check if coordinates are present in the response
    if 'coord' not in response or 'lat' not in response['coord'] or 'lon' not in response['coord']:
        print("Coordinates not found in the response.")
        return None, None

    lat, lon = response['coord']['lat'], response['coord']['lon']

    # Get forecast data
    forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()
    print("Forecast Response:", forecast_response)


    # Check if required keys are present in the current weather response
    if 'main' not in response or 'weather' not in response:
        print("Required keys not found in the current weather response.")
        return None, None

    # Extract weather data from the current weather response
    weather_data = {
        "city": city,
        "temperature": round(response['main']['temp'] - 273.15, 2),
        "description": response['weather'][0]['description'],
        "icon": response['weather'][0]['icon']
    }

    # Extract daily forecasts, handling missing or unexpected keys
    daily_forecasts = []
    for daily_data in forecast_response.get('daily', [])[:5]:
        temp_data = daily_data.get('temp', {})
        weather_data = daily_data.get('weather', [{}])[0]

        daily_forecasts.append({
            "day": datetime.datetime.fromtimestamp(daily_data.get('dt', 0)).strftime("%A"),
            "min_temp": round(temp_data.get('min', 0) - 273.15, 2),
            "max_temp": round(temp_data.get('max', 0) - 273.15, 2),
            "description": weather_data.get('description', ''),
            "icon": weather_data.get('icon', '')
        })

    return weather_data, daily_forecasts


