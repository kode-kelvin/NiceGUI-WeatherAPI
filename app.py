from nicegui import ui
from datetime import datetime
import httpx
from dotenv import load_dotenv
import os
load_dotenv()

# loading my api key from .env file  - you can replace os.getenv("API_KEY") with your API KEY
api_key = os.getenv("API_KEY")
base_url = 'http://api.openweathermap.org/data/2.5/weather?'


def check_city():
    params = {'q': city_name.value, 'appid': api_key}

# Make the API request using httpx
    with httpx.Client() as client:
        response = client.get(base_url, params=params)

# Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON data
            data = response.json()

# Check if the 'cod' key in the response indicates an error
            if data['cod'] == '404':
                print(f'City not found: {city_name}')
            else:
                # Extract relevant information
                main_info = data['main']
                temperature_kelvin = main_info['temp']
                temperature_celsius = round(temperature_kelvin - 273.15)
                humidity = main_info['humidity']
                weather_info = data['weather'][0]['description']
                icon_code = data['weather'][0]['icon']
                feels_like_temp = data['main']['feels_like']
                city = data['name']
                country = data['sys']['country']
                current_time = datetime.utcfromtimestamp(
                    data['dt'] + data['timezone']).strftime("%b %d, %Y %I:%M%p")

# --- showing the info in the interface ---
                temp.set_text(f'{temperature_celsius}°C')
                humidity_info.set_text(f'Humidity: {humidity}%')
                city_weather.set_text(f'{weather_info}')
                img.set_source(
                    f'https://openweathermap.org/img/wn/{icon_code}@2x.png')
                name_of_city.set_text(f'{city}, {country}')
                city_time.set_text(current_time)
                weather_feels.set_text(
                    f'Feels like: {round(feels_like_temp - 273.15)}°C')
# -- notify user if entry not found ---
        else:
            ui.notify('City not found', color='red')


# -- layout setup ---
cont = ui.column().classes('w-full md:w-2/4 sm:w-full').style("""
        margin: auto;""")
with cont:
    # -- accepting city input --
    city_name = ui.input(label="Enter city", placeholder='start typing..').props(
        'clearable').classes('w-full')
    ui.button('SEARCH WEATHER', on_click=check_city)  # triggering the function

# -- Display response or city info -- ---
    city_time = ui.label().classes('text-red-400')  # area
    name_of_city = ui.label().classes('text-3xl font-medium')  # city
    with ui.row():
        img = ui.image().classes('w-28')  # img
        temp = ui.label().classes('text-5xl font-bold')  # temp in celsuis
    weather_feels = ui.label()  # feels like
    city_weather = ui.label()  # description
    humidity_info = ui.label()  # humidity

# -- Run the app -- --
ui.run(title='MeteorMate', favicon="🔅", host='0.0.0.0', port=8006)
