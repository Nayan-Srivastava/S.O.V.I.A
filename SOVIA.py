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
        elif 'game' in query:
            
            speak("You can play three types of game that is key operated games...in which I have snake game, voice based games....in which I have Chess... and motion based games....in which I have Dinosaur Game. So, which one you would like to play..first..Second or third ")
            qry=takecommand().lower()
            if 'first' in qry:
                speak("flappy bird or snake game")
                inp=takecommand().lower()
# Snake Game
                if 'snake game' in inp:
                    snakeGame.snakegame()
            # Dinosaur Game
            if 'third' in qry:
                speak("Do you want to play Dinosaur game")
                inp=takecommand().lower()
                if 'yes' in inp:

                    import cv2
                    import numpy as np
                    import joblib
                    import pygame
                    from sys import exit
                    from random import randrange, choice
                    import os

                    jump_model = joblib.load('jump_model.pkl')
                    msg = ''


                    def convert_frame_to_model(Canny_image):

                        # 1 Step
                        width = 128
                        height = 96
                        dim = (width, height)
                        resized = cv2.resize(Canny_image, dim, interpolation=cv2.INTER_AREA)

                        # 2 Step
                        reshaped_image = resized.reshape(-1, resized.size)

                        # 3 Step
                        return jump_model.predict(reshaped_image)


                    cap = cv2.VideoCapture(0)

                    x = 800
                    y = 700

                    os.environ['SDL_VIDEO_WINDOW_POS'] = f'{(x, y)}'

                    THIS_FOLDER = os.getcwd()

                    pygame.init()

                    SCREEN_WIDTH = 840
                    SCREEN_HEIGHT = 680

                    WHITE = (255, 255, 255)
                    BLACK = (0, 0, 0)

                    FPS = 30
                    GAME_SPEED = 10
                    FLOOR_SPEED = 10
                    GAME_OVER = False

                    points = 0
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

                    song = 0

                    font = pygame.font.SysFont('comicsansms', 40, True, True)
                    score_sound = pygame.mixer.Sound(os.path.join(THIS_FOLDER, 'score_sound.wav'))
                    score_sound.set_volume(0.2)


                    class Dino(pygame.sprite.Sprite):
                        def __init__(self):
                            super().__init__()
                            self.jump_sound = pygame.mixer.Sound(os.path.join(THIS_FOLDER, 'jump_sound.wav'))
                            self.death_sound = pygame.mixer.Sound(os.path.join(THIS_FOLDER, 'death_sound.wav'))

                            self.up = False
                            self.stop = False
                            self.xpos = 50
                            self.ypos = (SCREEN_HEIGHT // 2) + 140
                            self.dino_imgs = [os.path.join(THIS_FOLDER, f'dinossaur{i}.png') for i in range(3)]

                            self.index = 0
                            self.image = pygame.image.load(self.dino_imgs[self.index]).convert_alpha()
                            self.mask = pygame.mask.from_surface(self.image)

                            self.image = pygame.transform.scale(self.image, (84, 84))
                            self.rect = self.image.get_rect()
                            self.rect[0], self.rect[1] = self.xpos, self.ypos

                        def collision(self):
                            global GAME_SPEED, FLOOR_SPEED
                            if pygame.sprite.spritecollide(dino, obstacle_group, False,
                                                           pygame.sprite.collide_mask) or pygame.sprite.spritecollide(dino,
                                                                                                                      flying_dino_group,
                                                                                                                      False,
                                                                                                                      pygame.sprite.collide_mask):
                                GAME_SPEED = 0
                                FLOOR_SPEED = 0
                                self.stop = True
                                flying_dino.stop = True

                        def jump(self):
                            self.jump_sound.play()
                            self.up = True

                        def update(self):
                            # JUMP CONDITION
                            if self.stop == False:
                                if self.up == False:
                                    if self.rect[1] < self.ypos:
                                        self.rect[1] += 20
                                    else:
                                        self.rect[1] = self.ypos
                                if self.up == True:
                                    if self.rect[1] <= self.ypos - 200:
                                        self.up = False
                                    else:
                                        self.rect[1] -= 30

                                # SPRITES
                                if self.index >= len(self.dino_imgs) - 1:
                                    self.index = 0
                                self.index += 0.25

                                self.image = pygame.image.load(self.dino_imgs[int(self.index)]).convert_alpha()
                                self.image = pygame.transform.scale(self.image, (128, 128))
                                self.mask = pygame.mask.from_surface(self.image)

                            else:
                                pass


                    class Flying_dino(pygame.sprite.Sprite):
                        def __init__(self):
                            super().__init__()
                            self.flying_dino_imgs = [os.path.join(THIS_FOLDER, f'fly_dino{i}.png') for i in range(2)]
                            self.stop = False
                            self.index = 0
                            self.image = pygame.image.load(self.flying_dino_imgs[self.index]).convert_alpha()
                            self.mask = pygame.mask.from_surface(self.image)

                            self.image = pygame.transform.scale(self.image, (84, 84))
                            self.rect = self.image.get_rect()
                            self.rect[0], self.rect[1] = SCREEN_WIDTH, (SCREEN_HEIGHT // 2)

                        def update(self):
                            # SPRITES
                            if self.stop == False:
                                if self.index >= len(self.flying_dino_imgs) - 1:
                                    self.index = 0

                                self.index += 0.25
                                self.image = pygame.image.load(self.flying_dino_imgs[int(self.index)]).convert_alpha()
                                self.image = pygame.transform.scale(self.image, (128, 128))
                                self.mask = pygame.mask.from_surface(self.image)
                            else:
                                pass


                    class Obstacle(pygame.sprite.Sprite):
                        def __init__(self):
                            super().__init__()
                            self.obstacle_imgs = [os.path.join(THIS_FOLDER, 'obstacle0.png')]

                            self.image = pygame.image.load(self.obstacle_imgs[0]).convert_alpha()
                            self.mask = pygame.mask.from_surface(self.image)
                            self.image = pygame.transform.scale(self.image, (84, 84))
                            self.rect = self.image.get_rect()
                            self.rect[0], self.rect[1] = SCREEN_WIDTH, (SCREEN_HEIGHT // 2) + 162
                            self.mask = pygame.mask.from_surface(self.image)


                    class Clouds(pygame.sprite.Sprite):
                        def __init__(self):
                            super().__init__()
                            self.cloud_imgs = [os.path.join(THIS_FOLDER, 'clouds0.png')]

                            self.image = pygame.image.load(self.cloud_imgs[0]).convert_alpha()
                            self.image = pygame.transform.scale(self.image, (148, 148))
                            self.rect = self.image.get_rect()
                            self.rect[0], self.rect[1] = (SCREEN_WIDTH // 2) + randrange(-400, 400, 100), (
                                        SCREEN_HEIGHT // 2) - randrange(200, 400, 100)

                        def update(self):
                            if self.rect.topright[0] < 0:
                                self.rect[0] = SCREEN_WIDTH
                                self.rect[1] = (SCREEN_HEIGHT // 2) - randrange(200, 400, 100)
                            self.rect[0] -= GAME_SPEED


                    class Floor(pygame.sprite.Sprite):
                        def __init__(self):
                            super().__init__()
                            self.floor_imgs = [os.path.join(THIS_FOLDER, 'floor0.png')]

                            self.image = pygame.image.load(self.floor_imgs[0]).convert_alpha()
                            self.image = pygame.transform.scale(self.image, (64, 64))
                            self.rect = self.image.get_rect()
                            self.rect[0], self.rect[1] = 0, SCREEN_HEIGHT // 2 + 200

                        def update(self):
                            if self.rect.topright[0] < 0:
                                self.rect[0] = SCREEN_WIDTH
                            self.rect[0] -= FLOOR_SPEED


                    dino = Dino()
                    dino_group = pygame.sprite.Group()
                    dino_group.add(dino)

                    flying_dino = Flying_dino()
                    flying_dino_group = pygame.sprite.Group()
                    flying_dino_group.add(flying_dino)

                    obstacle = Obstacle()
                    obstacle_group = pygame.sprite.Group()
                    obstacle_group.add(obstacle)

                    numb_of_clouds = 5
                    clouds_group = pygame.sprite.Group()
                    for c in range(numb_of_clouds):
                        clouds = Clouds()
                        clouds_group.add(clouds)

                    floor_group = pygame.sprite.Group()
                    for c in range(-64, SCREEN_WIDTH, 60):
                        floor = Floor()
                        floor.rect[0] = c
                        floor_group.add(floor)

                    clock = pygame.time.Clock()

                    obstacle_choice = choice([obstacle, flying_dino])

                    while True:
                        sucess, img = cap.read()

                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        imgCanny = cv2.Canny(gray, 155, 105)

                        model_prediction = convert_frame_to_model(imgCanny)

                        if model_prediction == 0:
                            msg = 'Not jumping'
                        else:
                            msg = 'Jumping'

                        cv2.putText(imgCanny, f'{msg}', (480 // 2, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
                        cv2.imshow('Canny', imgCanny)

                        if cv2.waitKey(1) & 0xff == ord('q'):
                            break

                        clock.tick(FPS)
                        screen.fill(WHITE)

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                exit()

                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_q:
                                    cap.release()
                                    cv2.destroyAllWindows()
                                    pygame.quit()
                                    exit()

                                if event.key == pygame.K_r and GAME_OVER == True:
                                    GAME_SPEED = 10
                                    FLOOR_SPEED = 10
                                    points = 0
                                    song = 0
                                    obstacle.rect[0] = SCREEN_WIDTH
                                    flying_dino.rect[0] = SCREEN_WIDTH
                                    dino.stop = False
                                    dino.rect[1] = dino.ypos
                                    flying_dino.stop = False

                        dino_group.draw(screen)
                        dino_group.update()
                        dino.collision()

                        flying_dino_group.draw(screen)
                        flying_dino_group.update()

                        obstacle_group.draw(screen)
                        obstacle_group.update()

                        clouds_group.draw(screen)
                        clouds_group.update()

                        floor_group.draw(screen)
                        floor_group.update()

                        text = font.render(f'{points}', True, BLACK)
                        screen.blit(text, (700, 40))

                        if model_prediction == 1:
                            if dino.rect[1] < dino.ypos:
                                pass
                            else:
                                dino.jump()

                        if obstacle_choice.rect.topright[0] < 0:
                            flying_dino.rect[0] = SCREEN_WIDTH
                            obstacle.rect[0] = SCREEN_WIDTH
                            obstacle_choice = choice([obstacle, flying_dino])
                        else:
                            obstacle_choice.rect[0] -= GAME_SPEED

                        if GAME_SPEED != 0:
                            points += 1
                            if (points % 100) == 0:
                                score_sound.play()
                                if GAME_SPEED == 46:
                                    pass
                                else:
                                    GAME_SPEED += 2
                        else:
                            points += 0
                            if song > 1:
                                song = 2
                            else:
                                song += 1
                            dino.jump_sound.stop()
                            txt = ['GAME OVER', 'Press R to play again', 'Press Q to Quit']
                            line1 = font.render(txt[0], True, BLACK)
                            line2 = font.render(txt[1], True, BLACK)
                            line3 = font.render(txt[2], True, BLACK)
                            screen.blit(line1, ((SCREEN_WIDTH // 2) - (line1.get_width() // 2), (SCREEN_HEIGHT // 2) - 100))
                            screen.blit(line2, ((SCREEN_WIDTH // 2) - (line2.get_width() // 2), (SCREEN_HEIGHT // 2) - 50))
                            screen.blit(line3, ((SCREEN_WIDTH // 2) - (line3.get_width() // 2), (SCREEN_HEIGHT // 2)))

                            GAME_OVER = True

                        if song == 1:
                            dino.death_sound.play()

                        pygame.display.flip()


                    def chalao():
                        cap.release()
                        cv2.destroyAllWindows()


                    chalao()
                    

        else:
            query = query
            
            try:
                try:
                    speak('Searching...')
                    res = client.query(query)
                    results = next(res.results).text
                    speak('WOLFRAM-ALPHA says - ')
                    speak('Got it.')
                    speak(results)

                except:
                    speak('Searching...')
                    results = wikipedia.summary(query, sentences=2)
                    speak('Got it.')
                    speak('WIKIPEDIA says - ')
                    speak(results)

            except:
                speak("speaks sir")
