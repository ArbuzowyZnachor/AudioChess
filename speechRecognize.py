import speech_recognition as sr
from gtts import gTTS as gs
import re
import os
from playsound import playsound

# import os

def getMove():
    r= sr.Recognizer()
    text = ""
    print("listining") #debug 
    with sr.Microphone() as source:
        audio = r.listen(source, 10, 4)
        try:
            text = r.recognize_google(audio, language="pl")
            text = text.replace(" ","").lower()
            print(text+"\n") #debug
        except:
            print("Error\n ") #debug
    match = re.match("[a-h][1-8][a-h][1-8]", text, flags=0)
    if match:
        return text
    else:
        return ""

def sayMove(move):
    moveText = " ".join(move)
    language = "ru"
    speech = gs(text=moveText, lang= language, slow=False)
    speech.save("text.mp3")
    playsound("text.mp3", False)
    os.remove("text.mp3")