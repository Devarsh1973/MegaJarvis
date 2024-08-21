import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI 
from gtts import gTTS
import pygame
import os
from datetime import datetime
import time
import pytz

recognizer = sr.Recognizer()
engine=pyttsx3.init()
newsapi="62c16585988f436abf0d9c4feb45bd27"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def get_weather(location):
    weather_api = "233edf34369771f5d67775c8e6f6722d"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "q=" + location + "&appid=" + weather_api + "&units=metric"
    
    response = requests.get(complete_url)
    weather_data = response.json()
    
    if weather_data["cod"] != "404":
        main = weather_data["main"]
        weather_description = weather_data["weather"][0]["description"]
        temperature = main["temp"]
        
        weather_info = f"The temperature in {location} is {temperature}°C with {weather_description}."
        speak(weather_info)
    else:
        speak("Sorry, I couldn't find the weather information for that location.")


import time
from datetime import datetime

def set_alarm(alarm_time):
    try:
        # Ensure the alarm_time is in "HH:MM" format
        datetime.strptime(alarm_time, "%H:%M")
    except ValueError:
        speak("Please provide the time in HH:MM format.")
        return

    speak(f"Alarm set for {alarm_time}.")
    
    while True:
        current_time = datetime.now().strftime("%H:%M")
        if current_time == alarm_time:
            speak("Wake up! It's time!")
            break
        time.sleep(30)  # Check every 30 seconds


def tell_time():
    est = pytz.timezone('US/Eastern')
    now = datetime.now(est)
    current_time = now.strftime("%H:%M:%S")
    return current_time

current_time_est = tell_time()
current_time_est

def tell_date():
    # Get the current date in EST
    est = pytz.timezone('US/Eastern')
    today = datetime.now(est).strftime("%B %d, %Y")
    speak(f"Today in EST is {today}.")

    
def aiProcess(command):
    client = OpenAI(api_key="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",)
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please."},
        {"role": "user", "content": command}
    ]
    )

    return completion.choices[0].message.content

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")


    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])
    else:
        output=aiProcess(c)
        speak(output)                    
       
if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
         
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("Ya")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)


        except Exception as e:
            print("Error; {0}".format(e))