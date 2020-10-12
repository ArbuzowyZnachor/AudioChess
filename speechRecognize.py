import speech_recognition as sr
import re
import pyttsx3 


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
    if text == "poddajsię":
        return "surrender"
    if match:
        return text
    else:
        return ""

def sayMove(move):
    moveText = ", ".join(move)
    converter = pyttsx3.init()
    converter.setProperty('rate', 140) 
    converter.setProperty('volume', 0.7) 
    converter.say(moveText)
    converter.runAndWait() 