import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import smtplib
import webbrowser as wb
import os
import pyautogui
import psutil
import pyjokes
import random
import requests
import json
import subprocess
import wolframalpha

import snakeGame

engine=pyttsx3.init()
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
# Initialize the converter
converter = pyttsx3.init()
# Set properties before adding
# Things to say
# Sets speed percent
# Can be more than 100
# converter.setProperty('rate', 140)
# Set volume 0-1
converter.setProperty('volume', 1)

# Funtion which makes the Assistant speak

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


# Function to tell Time

def time_():
    Time=datetime.datetime.now().strftime("%I:%M:%S")
    speak("Current time is..")
    speak(Time)

# Function to tell Date

def date():
    year=int(datetime.datetime.now().year)
    month=int(datetime.datetime.now().month)
    date=int(datetime.datetime.now().day)
    speak("The current date is")
    speak(date)
    speak(month)
    speak(year)

# Function for greetings

def greeting():
    hour=datetime.datetime.now().hour
    if hour>=6 and hour<12:
        speak("Good Morning Sir")
    if hour>=12 and hour<16:
        speak("Good Afternoon Sir")
    if hour>=16 and hour<=24:
        speak("Good Evening Sir")
    speak("SOVIA at your service, How Can I help you")

# Function to take commands form microphone

def takecommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold=1
        r.energy_threshold=4000
        audio=r.listen(source)
    try:
        print("Recognizing...")
        query=r.recognize_google(audio)

    except Exception as e:
        print(e)
        # speak("Sorry I didn't get that can you please repeat")
        return "None"
    return query

# Function to send Emails

def sendmail(to,content):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()#to send email
    server.login("voiceassistant846@gmail.com","jarvis@123")
    server.sendmail('voiceassistant846@gmail.com',to,content)
    server.close()


# function to take screenshot

def screenshot():
    img=pyautogui.screenshot()
    img.save("D:/Assistant/ss.png")

# funtion to tell about CPU percentage

def cpu():
    usage=str(psutil.cpu_percent())
    speak("CPU is at" + usage)

# function to tell battery percentage
def battery():
    battery=psutil.sensors_battery()
    speak("battery is at")
    speak(battery.percent)
    speak("percent")

# Function to tell joke

def jokes():
    speak(pyjokes.get_joke())

# Function to tell news

def news():

    url = (f"http://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=e38e33aa03d448068b70c4c1c2fed2f4")

    response = requests.get(url)
    t = response.text
    my_json = json.loads(t)
    speak("News for the day are")
    for i in range(0, 5):
        speak(my_json['articles'][i]['title'])
        speak("the description of above news is" + my_json['articles'][i]['description'])

# Function to tell features
def features():
    f=['Tell time','Tell date',
       'Tell a Joke','Tell a Current weather report and weather forecast for next day',
       'Search things in Wikipedia',
       'Send Emails through Gmail','Search in google chrome',
       'Shutdown the System','Logout the System','Restart the System',
       'Play songs','Switch Songs','Remember things',
       'Tell what you told me to remember','Take Screenshots',
       'Tell about CPU status','Tell battery Percentage',
       'Tell News','Open System application']
    for i in f:
        print(i)
    for i in f:
        speak(i)

#Function to answer questions
def answer():
    question =query
    app_id = '7WP4V3-7T4GPQX6EQ'
    client = wolframalpha.Client(app_id)
    res = client.query(question)
    answer = next(res.results).text
    print(answer)
    speak(answer)

def forecast(City):
    city_api_endpoint = "http://api.openweathermap.org/data/2.5/forecast?q="

    join_key = "&appid=" + "8e3aff6cd41e65082ba7285a185f00c4"
    units = "&units=metric"
    city_forecast = city_api_endpoint + City + join_key + units
    forecast_json = requests.get(city_forecast).json()
    if forecast_json["cod"] != "404":
        forecast = forecast_json['list'][6]['main']
        forecast_temperature = forecast['temp']
        forecast_pressure = forecast['pressure']
        forecast_humidity = forecast['humidity']
        forecast_main = forecast_json['list'][0]['weather'][0]['main']
        text1 = str("Tommorrow's Temperature is " + str(forecast_temperature) + "degree celsius" +
                    "\n atmospheric pressure is" + str(forecast_pressure) + "hectopascal" + "humidity is "
                    + str(forecast_humidity) + "percent" + "with " + str(forecast_main))
        speak(text1)

def weather():
    api_key = "93654f3dc80dd40be139ca13704330c4"
    # base_url variable to store url
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    speak("Please tell me your current city")

    # Give city name
    city_name = takecommand().lower()
    units = "&units=metric"

    # complete_url variable to store complete url address
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name+units

    # get method of requests module
    # return response object
    response = requests.get(complete_url)

    # json method of response object
    # convert json format data into
    # python format data
    x = response.json()

    # Now x contains list of nested dictionaries
    # Check the value of "cod" key is equal to
    # "404", means city is found otherwise,
    # city is not found
    if x["cod"] != "404":

        # store the value of "main"
        # key in variable y
        y = x["main"]
        current_temperature = y["temp"]
        current_temperature = current_temperature-273.15
        current_temperature = ('%.2f' % current_temperature)
        current_pressure = y["pressure"]
        current_humidiy = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        text=str(" Temperature " +
              str(current_temperature) +"degree celsius"+
              "\n atmospheric pressure is" +
              str(current_pressure) +"hectopascal"
              "\n humidity is " +
              str(current_humidiy) +"percent"+
              "with " +
              str(weather_description))
        speak(text)
        speak("Do you want to know weather forecast for tommorrow??")
        cmd=takecommand().lower()

        if "yes" or "weather forecast" in cmd:
            City = city_name
            forecast(City)
        elif "no" in cmd:
            speak("ok")

    else:
        print(" City Not Found ")

if __name__ == '__main__':
    greeting()
    while True:
        query=takecommand().lower()
        print(query)
        if "time" in query:
            time_()
        elif "date" in query:
            date()
        elif "offline" in query:
            speak("ok Sir")
            quit()
        elif "wikipedia" in query:
            speak("Sure sir let me check..")
            query=query.replace("wikipedia","")
            result=wikipedia.summary(query,sentences=2)
            speak(result)
        elif 'send email' in query:
            try:
                speak("What should I say")
                content=takecommand()
                speak("Please enter the receiver's emial address")
                to=input()
                sendmail(to,content)
                speak("Email sent successfully")
            except Exception as e:

                speak("Unable to send the email")
        elif 'search' in query:
            speak("What should I search for")
            chromepath="C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
            search=takecommand().lower()
            wb.get(chromepath).open_new_tab(search+".com")
        elif 'logout' in query:
            os.system("shutdown - l")  #for logout
        elif 'shutdown' in query:
            os.system("shutdown /s /t 1")  #for shutdown
        elif 'restart' in query:
            os.system("shutdown /r /t 1")  #for restart
        # to play song
        elif "play song" in query:
            songs_dir="D:/Music"
            songs=os.listdir(songs_dir)
            n=random.randint(0,len(songs))
            os.startfile(os.path.join(songs_dir,songs[n]))
        # to switch songs
        elif "play another song" in query:
            speak("Ok sir")
            songs_dir="D:/Music"
            songs=os.listdir(songs_dir)
            n=random.randint(0,len(songs))
            os.startfile(os.path.join(songs_dir,songs[n]))

        # to make assistant to remember something

        elif "remember that" in query:
            speak("What should I remember")
            data=takecommand()
            speak("you said me to remember" + data)
            remember=open("data.txt","w")
            remember.write(data)
            remember.close()

        # make assistant speak what you told to remember

        elif 'what i told you to remember' in query:
            remember=open("data.txt","r")
            speak("you said me to remember that" + remember.read())
        elif 'screenshot' in query:
            screenshot()
            speak("Screenshot taken")

        elif 'cpu' in query:
            cpu()
        elif 'battery' in query:
            battery()
        elif 'joke' in query:
            jokes()
        elif 'news' in query:
            news()
        # to open Visual Studio code
        elif 'open code' in query:
            speak("opening Visual Studio Code")
            codePath="C:\\Users\\NAYAN\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe" #write app's target here
            os.startfile(codePath)

        # to open Pycharm

        elif 'pycharm' in query:
            speak("opening Pycharm")
            codePath="C:\\Program Files\\JetBrains\PyCharm Community Edition 2020.1.3\\bin\\pycharm64.exe" #write app's target here
            os.startfile(codePath)
        # to open system apps
        elif 'wordpad' in query:
            speak("Opening Wordpad")
            subprocess.Popen('C:\\Windows\\System32\\write.exe')
        elif 'notepad' in query:
            speak("Opening notepad")
            subprocess.Popen('C:\\Windows\\System32\\notepad.exe')
        elif 'calculator' in query:
            speak("Opening calculator")
            subprocess.Popen('C:\\Windows\\System32\\calc.exe')
        elif 'word' in query:
            speak("Opening word")
            subprocess.Popen("C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE")
        elif 'powerpoint' in query:
            speak("Opening powerpoint")
            subprocess.Popen("C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE")
        elif 'excel' in query:
            speak("Opening excel")
            subprocess.Popen("C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE")
        elif 'photoshop' in query:
            speak("Opening photoshop")
            subprocess.Popen("C:\\Program Files (x86)\\Adobe\\Photoshop 7.0\\Photoshop.exe")
        elif 'what can you do' in query:
            speak("I can...")
            features()
        elif 'what' in query:
            answer()
        elif 'weather' in query:
            weather()
        elif 'play games' in query:
            
            speak("three types of games you can play, first is key operated games in which you can play snake game,second is voice based games in which you can play chess and third is motion detection game in which you can play dinasore game. so which one you want to play..first..Second or third ")
            qry=takecommand().lower()
            if 'first' in qry:
                speak("flappy bird or snake game")
                inp=takecommand().lower()
                
                if 'snake game' in inp:
                    snakeGame.snakegame()
                    

        else:
            query = query
            speak('Searching...')
            try:
                try:
                    res = client.query(query)
                    results = next(res.results).text
                    speak('WOLFRAM-ALPHA says - ')
                    speak('Got it.')
                    speak(results)

                except:
                    results = wikipedia.summary(query, sentences=2)
                    speak('Got it.')
                    speak('WIKIPEDIA says - ')
                    speak(results)

            except:
                wb.open('www.google.com')
