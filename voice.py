import pyttsx3
import speech_recognition as sr
import pywhatkit
import wikipedia
import webbrowser
import datetime
import requests

from bs4 import BeautifulSoup
import os
import pyautogui
from plyer import notification
from pygame import mixer

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 170)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source, 0, 4)
    try:
        print("Understanding..")
        query = r.recognize_google(audio, language='en-in')
        print(f"You Said: {query}\n")
    except Exception as e:
        print("Say that again")
        return "None"
    return query.lower()


def searchGoogle(query):
    if "google" in query:
        query = query.replace("google", "")
        speak("This is what I found on Google")
        try:
            pywhatkit.search(query)
        except:
            speak("No speakable output available")


def searchYoutube(query):
    if "youtube" in query:
        speak("This is what I found for your search!")
        query = query.replace("youtube", "")
        web = "https://www.youtube.com" + query
        webbrowser.open(web)
        pywhatkit.playonyt(query)
        speak("Done, Sir")


def searchWikipedia(query):
    if "wikipedia" in query:
        speak("Searching from Wikipedia....")
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia..")
        print(results)
        speak(results)


if __name__ == "__main__":
    while True:
        query = takeCommand()
        if "hello" in query:
            speak("Yes sir, How can I assist you?")
            while True:
                query = takeCommand()
                if "go to sleep" in query:
                    speak("Ok sir, You can call me anytime")
                    break
                elif "hello" in query:
                    speak("Hello sir, how are you?")
                elif "i am fine" in query:
                    speak("That's great, sir")
                elif "how are you" in query:
                    speak("Perfect, sir")
                elif "thank you" in query:
                    speak("You are welcome, sir")

                elif "pause" in query:
                    pyautogui.press("k")
                    speak("video paused")
                elif "play" in query:
                    pyautogui.press("k")
                    speak("video played")
                elif "mute" in query:
                    pyautogui.press("m")
                    speak("video muted")

                elif "volume up" in query:
                    from keyboard import volumeup
                    speak("Turning volume up,sir")
                    volumeup()
                elif "volume down" in query:
                    from keyboard import volumedown
                    speak("Turning volume down, sir")
                    volumedown()

                
                elif "open" in query:
                    from Dictapp import openappweb
                    openappweb(query)
                elif "close" in query:
                    from Dictapp import closeappweb
                    closeappweb(query)

                
                elif "remember that" in query:
                    rememberMessage = query.replace("remember that", "")
                    rememberMessage = rememberMessage.replace("jarvis", "")  # Corrected this line
                    speak("You told me to " + rememberMessage)  # Added space after 'to'
                    remember = open("Remember.txt", "a")
                    remember.write(rememberMessage + "\n")  # Added a newline after each message
                    remember.close()
                elif "what do you remember" in query:
                    remember = open("Remember.txt", "r")
                    speak("You told me to " + remember.read())  # Added space after 'to'
                    remember.close()

                elif "screenshot" in query:
                     import pyautogui #pip install pyautogui
                     im = pyautogui.screenshot()
                     im.save("ss.jpg")

                elif "click my photo" in query:
                        pyautogui.press("super")
                        pyautogui.typewrite("camera")
                        pyautogui.press("enter")
                        pyautogui.sleep(2)
                        speak("SMILE")
                        pyautogui.press("enter")

                elif 'type' in query:
                    query = query.replace("type","")
                    pyautogui.typewrite(f"{query}",0.1)


                
                elif "temperature" in query:
                    search = "temperature in Mumbai"
                    url = f"https://www.google.com/search?q={search}"
                    r  = requests.get(url)
                    data = BeautifulSoup(r.text,"html.parser")
                    temp = data.find("div", class_ = "BNeawe").text
                    speak(f"current{search} is {temp}")
                elif "weather" in query:
                    search = "temperature in Mumbai "
                    url = f"https://www.google.com/search?q={search}"
                    r  = requests.get(url)
                    data = BeautifulSoup(r.text,"html.parser")
                    temp = data.find("div", class_ = "BNeawe").text
                    speak(f"current{search} is {temp}")

                elif "the time" in query:
                    strTime = datetime.datetime.now().strftime("%H:%M")    
                    speak(f"Sir, the time is {strTime}")


                elif "calculate" in query:
                    from Calculatenumbers import WolfRamAlpha
                    from Calculatenumbers import Calc
                    query = query.replace("calculate","")
                    query = query.replace("jarvis","")
                    Calc(query)

                elif "shutdown the system" in query:
                    speak("Are You sure you want to shutdown")
                    shutdown = input("Do you wish to shutdown your computer? (yes/no)")
                    if shutdown == "yes":
                        os.system("shutdown /s /t 1")

                    elif shutdown == "no":
                        break

                elif "schedule my day" in query:
                    tasks = [] #Empty list 
                    speak("Do you want to clear old tasks (Plz speak YES or NO)")
                    query = takeCommand().lower()
                    if "yes" in query:
                        file = open("tasks.txt","w")
                        file.write(f"")
                        file.close()
                        no_tasks = int(input("Enter the no. of tasks :- "))
                        i = 0
                        for i in range(no_tasks):
                            tasks.append(input("Enter the task :- "))
                            file = open("tasks.txt","a")
                            file.write(f"{i}. {tasks[i]}\n")
                            file.close()
                    elif "no" in query:
                        i = 0
                        no_tasks = int(input("Enter the no. of tasks :- "))
                        for i in range(no_tasks):
                            tasks.append(input("Enter the task :- "))
                            file = open("tasks.txt","a")
                            file.write(f"{i}. {tasks[i]}\n")
                            file.close()

                    elif "show my schedule" in query:
                        file = open("tasks.txt","r")
                        content = file.read()
                        file.close()
                        mixer.init()
                        mixer.music.load("notification.mp3.wav")
                        mixer.music.play()
                        notification.notify(
                            title = "My schedule :-",
                            message = content,
                            timeout = 15
                            )
                        
                    



                elif "finally sleep" in query:
                    speak("Going to sleep,sir")
                    exit()


                else:
                    searchGoogle(query)
                    searchYoutube(query)
                    searchWikipedia(query)


            
                    
                

                
