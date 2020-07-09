import speech_recognition as sr
import re

def getMove():
    r= sr.Recognizer()
    text = ""
    print("listining") #debug 
    with sr.Microphone() as source:
        audio = r.listen(source, 3, 4)
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