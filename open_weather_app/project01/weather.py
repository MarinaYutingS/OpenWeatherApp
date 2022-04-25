
from tkinter import messagebox
from tokenize import String
import requests
import tkinter as tk
from tkinter import StringVar, messagebox
from PIL import Image, ImageTk
import time

HEIGHT = 600 
WIDTH = 700 

root = tk.Tk()
root.title("Weather App")


# function format_response()
# input: weather data in json format
# output: weather data in string 
def format_response(weather):
    try:
        name = weather['name']
        description = weather['weather'][0]['description']
        tempt_cel = weather['main']['temp']
        tempt_fah = round((tempt_cel * (9/5) + 32),2)
        humidity = weather['main']['humidity']
        wind = weather['wind']['speed']

        final_str =  'City: %s \nConditions: %s \n\nTemperature (°C ): %s\nTemperature (°F ): %s\n\nHumidity: %s\nWind Speed: %s' %(name, description, tempt_cel, tempt_fah, humidity, wind)
    except:
        final_str = 'There was a problem retrieving the information'
    return final_str

def get_weather(city):
    # api key
    weather_key = 'd415efd7be5aeba7619d5ed64dde34bc'
    # define url
    url = 'https://api.openweathermap.org/data/2.5/weather'
    # define params as a dictionary to pass requests to the server
    params = {'APPID': weather_key, 'q' : city, 'units': 'metric' }
    #get requests
    response = requests.get(url,params=params)
    # get response in json format 
    weather = response.json()

    lbl_weather_info['text'] = format_response(weather)

    # get the weather icon
    icon_name = weather['weather'][0]['icon']
    open_image(icon_name)

    # start the countdown clock
    countdown()

def open_image(icon):
    size = int(lower_frame.winfo_height()*0.25)
    img = ImageTk.PhotoImage(Image.open('./img/'+icon+'.png').resize((size,size)))
    weather_icon.delete("all")
    weather_icon.create_image(0,0,anchor='nw',image=img)
    weather_icon.image = img

def countdown():
    temp = int(minute.get())*60 + int(second.get()) # 1800 sec = 30 mins
    # divmod(firstvalue = temp//60, secondvalue = temp%60)
    while temp > -1: 
        mins,secs = divmod(temp,60)
        # using format() method to strore the value up to two deciaml places
        minute.set("{0:2d}".format(mins))
        second.set("{0:2d}".format(secs))
        # updating the GUI window after decrementing the temp value every time
        time_frame.update()
        time.sleep(1)
        # when temp value = 0; pop up a messagebox 
        if (temp == 0):
            messagebox.showinfo("Time Countdown","Wether condition in "+entry.get()+" updated")
            minute.set("30")
            second.set("00")
            time_frame.update()
            get_weather(entry.get())
        # decrement temp value by every second
        temp -= 1  

# make a container to place the button in
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

# define and set a background image
background_image = tk.PhotoImage(file='project01/bg1.png')
background_label = tk.Label(root, image=background_image)
background_label.place(relheight=1,relwidth=1)

# crete a frame and center
frame = tk.Frame(root,bg='#80c1ff',bd = 5)
frame.place(relx = 0.5, rely = 0.1, relwidth=0.75, relheight=0.1,anchor='n')

# create an entry bar
entry = tk.Entry(frame, font=('Kefa',18))
# place the entry
entry.place(relwidth=0.65, relheight=1)

# add a button and palce the button in the root
# pass function to the button click event
button = tk.Button(frame, text="Get Weather",font=('Kefa',18), command=lambda: get_weather(entry.get()))
# place the button
button.place(relx=0.7,relwidth=0.3,relheight=1)

# ------------------------------------------------------------

lower_frame = tk.Frame(root, bg = '#80c1ff', bd = 10)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75,relheight=0.6,anchor='n')

# create a label widget and place into the frame
lbl_weather_info = tk.Label(lower_frame, font=('Kefa',20))
# place the label
lbl_weather_info.place(relwidth=1, relheight=1)

# create a canvas to hold the weather icon
weather_icon = tk.Canvas(lbl_weather_info, bg='white', bd=0, highlightthickness=0)
weather_icon.place(relx=0.75, rely=0, relwidth=1, relheight=0.5)
# print(tk.font.families())

# ------------------------------------------------------------

# create a frame show the time
time_frame = tk.Frame(root,bg='#80c1ff',bd = 5)
time_frame.place(relx=0.5, rely=0.87, relwidth=0.75,relheight=0.1,anchor='n')

# TODO minute: 30; second: 00
minute = tk.StringVar(time_frame, '30')
second = tk.StringVar(time_frame,'00')

txt_lbl = tk.Label(time_frame,text="Cout Down Clock",width = 3, font=('Kefa',15))
txt_lbl.place(relx=0.1, relwidth=0.3, relheight=1)

minute_lbl = tk.Label(time_frame,width = 3, font=('Kefa',15), textvariable=minute)
minute_lbl.place(relx=0.5,relwidth=0.15, relheight=1)

txt_lbl = tk.Label(time_frame,text=":",bg = '#80c1ff',width = 3, font=('Kefa',12))
txt_lbl.place(relx=0.7, relwidth=0.05, relheight=1)

second_lbl = tk.Label(time_frame,width = 3, font=('Kefa',15),textvariable=second)
second_lbl.place(relx=0.8, relwidth=0.15, relheight=1)


# ------------------------------------------------------------


root.mainloop()