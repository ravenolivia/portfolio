# API Weather Application
# Retrieves coordinates and weather forecast for user-specified city
# Uses Open-Meteo Geocoding and Forecast APIs
# Generates a weather report along with activity recommendations
# based on weather forecast
#====================================================================

import requests
from datetime import datetime
from zoneinfo import ZoneInfo

# translates Open-Meteo's weather codes to condition descriptions
weather_descriptions = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm"
}

# Retrieves latitude, longitude, and other location info
# for user's requested city
def get_coordinates(city_name):
    GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
    
    params = {
        "name": city_name,
        "count": 1,		# Limits to best match city only
        "language": "en"	# English language specified
    }
    
    try:
        response = requests.get(GEOCODING_URL, params=params)	# Sends request to Geocoding API
        response.raise_for_status()	#HTPPError if request unsuccessful
        location_data = response.json()		# Process returned JSON data
 
# Returns first matching location       
        if "results" in location_data and len(location_data["results"]) > 0:
            best_match = location_data["results"][0]
            
            location_info = {
                "name": best_match.get("name"),
                "country": best_match.get("country"),
                "admin1": best_match.get("admin1"),
                "latitude": best_match.get("latitude"),
                "longitude": best_match.get("longitude"),
                "timezone": best_match.get("timezone"),
            }
            return location_info

        else:
            print(f"Sorry, no results were found for '{city_name}'.")
            return None

# Error-handling for connection or API errors
    except requests.exceptions.RequestException as e:
        print(f"Geocoding error: {e}")
        return None

# Retrieves weather conditions for specified coordinates

def get_weather(latitude, longitude):
    WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,weather_code",
        "temperature_unit": "fahrenheit"
    }
 
# Requests current weather conditions from Open-Meteo    
    try:
        response = requests.get(WEATHER_URL, params=params)
        response.raise_for_status()	#HTPPError if request unsuccessful
        weather_data = response.json()		# Process returned JSON data
    
        return weather_data["current"]
 
# Error-handling for connection or API errors   
    except requests.exceptions.RequestException as e:
        print(f"Weather error: {e}")
        return None

# Gives brief suggestion of activities based on weather forecast (temp, weather code)
def get_activity_recommendations(weather_code, temperature):
    
    if weather_code in [0, 1, 2, 3] and 85 >= temperature >= 75:
        return "The world is your oyster! Beautiful weather for outdoor activities. Ride a bike, take a hike, go to the beach, or enjoy some nice A/C."
    elif weather_code in [0, 1, 2] and temperature > 85:
        return "Stay safe in the heat! Go swimming or keep outdoor activities limited to morning and evening. Indoor activities such as gaming, movies, art projects, etc are recommended."
    elif weather_code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
        return "Indoor activities may be best today. Stay home and game, go see a movie, or go to the museum!"
    elif weather_code in [71, 73, 75]:
        return "For the adventurous souls, skiing, snowboarding, or mountaineering may be possible today! Otherwise, perhaps a cozy day indoors with a hot chocolate and good book?"
    elif weather_code == 95:
        return "Severe weather calls for home activities such as reading, gaming, doing a puzzle, or trying a new recipe. Be prepared to seek shelter if necessary!"
    else:
        return "Consider the expected conditions before proceeding with outdoor activities today!"

# Returns brief summary of expected weather conditions corresponding with weather code
def weather_summary(weather_code):
    if weather_code == 0:
        return "Expect beautiful, clear skies today! ☀"
    elif weather_code in [1, 2, 3]:
        return "Expect some cloudy skies today. ☁"
    elif weather_code in [51, 53, 55, 61, 80]:
        return "Light rain is expected today. 🌧"
    elif weather_code in [63, 65, 81, 82]:
        return "Expect heavy rain today. Don't forget your umbrella! ☂"
    elif weather_code == 95:
        return "Thunderstorms and lightning are expected today. Stay safe! 🌩"
    elif weather_code in [71, 73, 75]:
        return "Snow is likely today! ❄"
    elif weather_code in [45, 48]:
        return "It may be foggy today. Careful on the road!"
    else:
        return "Check your local news for expected weather conditions."
    
# Generates summary of weather conditions for user-specified location
def display_weather_report(location):
# Generates current time in location based on timezone
    current_time = datetime.now(ZoneInfo(location["timezone"]))
    
    print("\nI found a matching location!")
    print(f"{'City:':<15} {location['name']}")
    print(f"{'State/Region:':<15} {location['admin1']}")
    print(f"{'Country:':<15} {location['country']}")
    print(f"{'Latitude:':<15} {location['latitude']}")
    print(f"{'Longitude:':<15} {location['longitude']}")
    print(f"{'Current Time:':<15} {current_time.strftime('%I:%M %p')}")
    print("-" * 60)
    
    weather = get_weather(
        location["latitude"],
        location["longitude"]
    )
    
    if weather:
        weather_code = weather["weather_code"]
        temperature = weather["temperature_2m"]
 
# Translates weather code into its text description           
        description = weather_descriptions.get(weather_code, "Unknown")
        
        print(f"Let's take a look at the weather report for {location['name']}:")
        print(f"\n{'Current Temperature:':<25} {weather['temperature_2m']}°F")
        print(f"{'Humidity:':<25} {weather['relative_humidity_2m']}%")
        print(f"{'Current Conditions:':<25} {description}")
        print("\n" + weather_summary(weather_code))
        print("\n" + get_activity_recommendations(weather_code, temperature))
    
# Main app loop which will run until user exits 
def main():
    while True:

# Prompts user for city name        
        city_name = input("Enter a city name to check the weather: ")
        location = get_coordinates(city_name)

# Displays location and forcast information if match is found
        if location:
            display_weather_report(location)

# Verifies choice to continue program, adds error-handling for invalid response        
        while True:
        
            again = input("\nSearch another city? Type yes or no: ").strip().lower()
        
            if again in ("yes", "y"):
                break
            elif again in ("no", "n"):
                print("Thank you for using my weather app! Enjoy your day!")
                return
            else:
                print("Invalid input. Please respond yes or no.")

# Starts main program        
if __name__ == "__main__":
    main()