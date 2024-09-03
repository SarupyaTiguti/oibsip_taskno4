import tkinter as tk
from tkinter import messagebox, ttk
import requests
from PIL import Image, ImageTk  # Pillow library for image processing

# Replace with your OpenWeatherMap API key
API_KEY = '183082789b59fd8357917a0787496c8b'

def get_weather_data(city, units='metric'):
    """
    Fetch weather data from OpenWeatherMap API.
    """
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': API_KEY,
        'units': units
    }
    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 401:
            messagebox.showerror("Unauthorized", "API key is invalid or not authorized. Please check your API key.")
            return None
        response.raise_for_status()  # Raise an error for other bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to retrieve data: {e}")
        return None

def display_weather(weather_data, units):
    """
    Display the weather data on the GUI.
    """
    if weather_data:
        city_name = weather_data['name']
        country = weather_data['sys']['country']
        weather = weather_data['weather'][0]
        temp = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        wind_speed = weather_data['wind']['speed']
        icon_code = weather['icon']

        # Update GUI elements with weather data
        location_label.config(text=f"{city_name}, {country}")
        temperature_label.config(text=f"Temperature: {temp}°{'C' if units == 'metric' else 'F'}")
        feels_like_label.config(text=f"Feels like: {feels_like}°{'C' if units == 'metric' else 'F'}")
        weather_label.config(text=f"Condition: {weather['description'].capitalize()}")
        wind_label.config(text=f"Wind Speed: {wind_speed} m/s")

        # Load and display weather icon
        load_weather_icon(icon_code)
def load_weather_icon(icon_code):
    """
    Load weather icon from OpenWeatherMap and display it.
    """
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
    response = requests.get(icon_url, stream=True)
    if response.status_code == 200:
        image_data = response.raw
        image = Image.open(image_data)
        image = image.resize((100, 100), Image.LANCZOS)  # Use LANCZOS instead of ANTIALIAS
        photo = ImageTk.PhotoImage(image)
        icon_label.config(image=photo)
        icon_label.image = photo
    else:
        messagebox.showerror("Error", "Failed to load weather icon.")


def fetch_weather():
    """
    Fetch weather data based on user input and update the display.
    """
    city = city_entry.get()
    if not city:
        messagebox.showerror("Input Error", "Please enter a city name.")
        return

    units = 'metric' if unit_var.get() == 'Celsius' else 'imperial'
    weather_data = get_weather_data(city, units)
    if weather_data:
        display_weather(weather_data, units)

# Initialize main window
window = tk.Tk()
window.title("Weather App")

# Location input
tk.Label(window, text="Enter City:").grid(row=0, column=0, padx=10, pady=5)
city_entry = tk.Entry(window)
city_entry.grid(row=0, column=1, padx=10, pady=5)

# Unit selection
unit_var = tk.StringVar(value='Celsius')
unit_dropdown = ttk.Combobox(window, textvariable=unit_var, values=['Celsius', 'Fahrenheit'])
unit_dropdown.grid(row=0, column=2, padx=10, pady=5)

# Fetch weather button
tk.Button(window, text="Fetch Weather", command=fetch_weather).grid(row=1, column=0, columnspan=3, pady=10)

# Display weather data
location_label = tk.Label(window, text="", font=('bold', 14))
location_label.grid(row=2, column=0, columnspan=3)

temperature_label = tk.Label(window, text="")
temperature_label.grid(row=3, column=0, columnspan=3)

feels_like_label = tk.Label(window, text="")
feels_like_label.grid(row=4, column=0, columnspan=3)

weather_label = tk.Label(window, text="")
weather_label.grid(row=5, column=0, columnspan=3)

wind_label = tk.Label(window, text="")
wind_label.grid(row=6, column=0, columnspan=3)

icon_label = tk.Label(window)
icon_label.grid(row=7, column=0, columnspan=3)

# Start the Tkinter event loop
window.mainloop()
