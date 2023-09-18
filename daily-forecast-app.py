from datetime import datetime
from tkinter import *
from timezonefinder import *
from PIL import Image, ImageTk
from urllib.request import urlopen
import tkinter as tk
import pytz
import requests


def get_image(url_id):
    url = f'https://openweathermap.org/img/wn/{url_id}@2x.png'
    url = urlopen(url)
    data = url.read()
    url.close()
    return data


def forecast_window(condition, temperature, humidity, feels_like, pressure,
                    weather_desc, wind_speed, current_time, icon):
    global condition_icon_img
    condition_stats.configure(text=f'{condition} | Feels like {int(feels_like)}°C')
    temp_stats.configure(text=f'{int(temperature)}°C')
    humidity_stats.configure(text=humidity)
    pressure_stats.configure(text=pressure)
    description_stats.configure(text=weather_desc)
    wind_stats.configure(text=wind_speed)
    clock.configure(text=current_time)
    place_name.configure(text='Current Time')
    condition_icon_img = ImageTk.PhotoImage(data=icon)
    condition_icon.configure(image=condition_icon_img)
    not_found.configure(text='')


def get_city_coords(name):
    response = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q='
                            f'{name},{COUNTRY_CODE}&limit={5}&appid={API_KEY}')
    if response.status_code == 200:
        data = response.json()
        try:
            main_info = data[0]
            lat = main_info['lat']
            lon = main_info['lon']
            return [lat, lon]
        except IndexError:
            not_found.configure(text='City not found.')
            return None, None


def get_weather(city_name):
    lat, lon = get_city_coords(city_name)
    if lat is None:
        return
    params = {'lat': lat, 'lon': lon, 'units': 'metric', 'appid': API_KEY}
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        obj = TimezoneFinder()
        result = obj.timezone_at(lng=lon, lat=lat)
        home = pytz.timezone(result)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%I:%M %p")
        data = response.json()
        main_info = data['main']
        temperature = main_info['temp']
        humidity = main_info['humidity']
        feels_like = main_info['feels_like']
        pressure = main_info['pressure']
        weather_desc = data['weather'][0]['description']
        condition = data['weather'][0]['main']
        wind_speed = data['wind']['speed']
        icon = data['weather'][0]['icon']
        icon = get_image(icon)
        forecast_window(condition, temperature, humidity, feels_like,
                        pressure, weather_desc, wind_speed, current_time, icon)


def get_input_data():
    city_name = textfield.get()
    get_weather(city_name)


API_KEY = '...'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
COUNTRY_CODE = 'ISO3166'

root = tk.Tk()
root.title("Daily Forecast")
root.geometry("900x500+300+200")
root.resizable(False, False)
root.configure(bg='white')

search_image = PhotoImage(file='search_bar.png')
my_image = Label(image=search_image, bg='white')
my_image.place(x=20, y=20)

textfield = Entry(root, justify='center', width=17, font=('poppins', 25, 'bold'), bg='#404040', border=0, fg='white')
textfield.place(x=50, y=40)
textfield.focus()

search_icon = PhotoImage(file='search_icon.png')
my_image_icon = Button(image=search_icon, borderwidth=0, cursor='hand2', bg='#404040', command=get_input_data)
my_image_icon.place(x=400, y=34)

logo_image = PhotoImage(file='main.png')
logo = Label(image=logo_image, bg='white')
logo.place(x=150, y=100)

box_image = PhotoImage(file='info_box.png')
box = Label(image=box_image, bg='white')
box.pack(padx=5, pady=5, side=BOTTOM)

label1 = Label(root, text='WIND', font=('Helvetica', 15, 'bold'), fg='white', bg='#1ab5ef')
label1.place(x=120, y=400)

label2 = Label(root, text='HUMIDITY', font=('Helvetica', 15, 'bold'), fg='white', bg='#1ab5ef')
label2.place(x=250, y=400)

label3 = Label(root, text='DESCRIPTION', font=('Helvetica', 15, 'bold'), fg='white', bg='#1ab5ef')
label3.place(x=430, y=400)

label4 = Label(root, text='PRESSURE', font=('Helvetica', 15, 'bold'), fg='white', bg='#1ab5ef')
label4.place(x=650, y=400)

not_found = Label(font=('arial', 30, 'bold'), fg='#ee666d', bg='white')
not_found.place(x=500, y=35)

place_name = Label(root, font=('arial', 15, 'bold'), bg='white')
place_name.place(x=30, y=100)
clock = Label(root, font=('Helvetica', 20), bg='white')
clock.place(x=30, y=130)

temp_stats = Label(font=('arial', 60, 'bold'), fg='#ee666d', bg='white')
temp_stats.place(x=400, y=150)
condition_icon = Label(image='', bg='white')
condition_icon.place(x=600, y=170)
condition_stats = Label(font=('arial', 15, 'bold'), bg='white')
condition_stats.place(x=400, y=240)

wind_stats = Label(text='...', font=('arial', 20, 'bold'), bg='#1ab5ef')
wind_stats.place(x=120, y=430)
humidity_stats = Label(text='...', font=('arial', 20, 'bold'), bg='#1ab5ef')
humidity_stats.place(x=285, y=430)
description_stats = Label(text='...', font=('arial', 20, 'bold'), bg='#1ab5ef')
description_stats.place(x=443, y=430)
pressure_stats = Label(text='...', font=('arial', 20, 'bold'), bg='#1ab5ef')
pressure_stats.place(x=670, y=430)

root.mainloop()
