import speech_recognition as sr
import re
import pyttsx3 
import sys

piecesDict = {
    "król":"K",
    "hetman":"Q",
    "goniec":"B",
    "skoczek":"N",
    "koczek":"N",
    "wieża":"R",
    "roszada":"O-O",
    "krótkaroszada":"O-O",
    "długaroszada": "O-O-O",
    "ch": "h",
}

# def getMove():
#     r= sr.Recognizer()
#     text = ""
#     print("listining") # DEBUG 
#     with sr.Microphone() as source:
#         audio = r.listen(source, 10, 4)
#         try:
#             text = r.recognize_google(audio, language="pl")
#             text = text.replace(" ","").lower()
#             print(text+"\n") # DEBUG
#         except:
#             print("Error\n ") # DEBUG
#     if text == "poddajsię":
#         return "surrender"
#     match = re.match("[a-h][1-8][a-h][1-8]", text, flags=0)
#     if match:
#         return text
#     else:
#         return ""

def getMoveBetter():
    r= sr.Recognizer()
    text = ""
    print("listining") # DEBUG 
    with sr.Microphone() as source:
        audio = r.listen(source, 10, 4)
        try:
            text = r.recognize_google(audio, language="pl")
            print(text+"\n") # DEBUG
            text = replacer(text)
            text = text.replace(" ","").lower()
            print(text+"\n") # DEBUG
        except:
            print("Error\n ") # DEBUG
    if text == "poddajsię":
        return "surrender"

    # match = re.match("[a-h][1-8][a-h][1-8]", text, flags=0)
    
    if text:
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

def sayWords(text):
    converter = pyttsx3.init()
    converter.setProperty('rate', 140) 
    converter.setProperty('volume', 0.7) 
    converter.say(text)
    converter.runAndWait() 

def replacer(text):
    for x in piecesDict:
        text = text.replace(x, piecesDict[x])
    return text