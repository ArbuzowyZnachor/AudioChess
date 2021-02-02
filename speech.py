import speech_recognition as sr
import re
import pyttsx3 
from playsound import playsound
import logging

#======================== Microphone input function ==========================

# Listen microphone input and return as a text
def listen():
    playsound("sound/mic.mp3")
    recognizer = sr.Recognizer()
    text = ""
    with sr.Microphone() as source:
        try:
            audio = recognizer.listen(source, 2, 4)
            text = recognizer.recognize_google(audio, language="pl")
        except Exception as ex:
                    logging.exception("listen function failed:", ex)
    if text == "":
        playsound("sound/error.mp3")
    return text

#======================== Replacer function and dictionaries =================

def replacer(text, dictionary):
    for x in dictionary:
        text = text.replace(x, dictionary[x])
    return text

player_move_dict = {
    "pionek": "",
    "pion": "",
    "król":"K",
    "hetman":"Q",
    "goniec":"B",
    "skoczek":"N",
    "wieża":"R",
    "długaroszada": "O-O-O",
    "krótkaroszada":"O-O",
    "roszada":"O-O",
    "ch": "h",
    "koniec": "B",
    "koczek":"N",
    "lew": "f",
    "-": ""}

move_dict = {
    'd': "de ", 
    'f': "ef ", 
    'h': "ha ", 
    "=Q": "promocja do hetmana",
    "=R": "promocja do wieży",
    "=B": "promocja do gońca",
    "=N": "promocja do skoczka",
    "K": "król ",
    "Q": "hetman ",
    "B": "goniec ",
    "N": "skoczek ",
    "R": "wieża ",
    "O-O-O": "długaroszada " ,
    "O-O": "krótkaroszada ",
    "x": "bije ",
    "+": ""}

level_dict = {
    "jeden": "1",
    "dwa": "2",
    "trzy": "3",
    "cztery": "4",
    "pięć": "5",
    "sześć": "6",
    "siedem": "7",
    "osiem": "8"}

#======================== Pages action functions =============================

def get_main_menu_action():
    data = {}
    text = listen()
    if(text):
        text = text.replace(" ","").lower()
        if(re.search("(gre|grę|gra|zacznij|rozpocznij|uruchom|start)", text)):
            data["action"] = "play"
        elif(re.search("(ustawienia|opcje)", text)):
            data["action"] = "settings"
        elif(re.search("(wyjś|zakończ|zamknij|wyjdź|powrót|wróc)", text)):
            data["action"] = "exit"  
        elif(re.search("(pomoc|instrukcj|corobić|jak|pomóż)", text)):
            data["action"] = "help"
            data["helpMessage"] = "Dostępne komendy to: rozpocznij grę, ustawienia oraz wyjście"
        else:
            data["action"] = "error"
            data["errorMessage"] = "Nieprawidłowa opcja"
    else:
        data["action"] = "none"
    return data

def get_game_menu_action():
    data = {}
    text = listen()
    if(text):
        text = text.replace(" ","").lower()
        if(re.search("(komputer|sam|solo|pc)", text)):
            data["action"] = "single"
        elif(re.search("(multi|online|sieć|siec)", text)):
            data["action"] = "multi"
        elif(re.search("(powrót|wróć|wraca|wyjście|zakończ|zamknij|wyjdź|progr)", text)):
            data["action"] = "exit"  
        elif(re.search("(pomoc|instrukcj|corobić|jak|pomóż)", text)):
            data["action"] = "help"
            data["helpMessage"] = "Dostępne komendy to: gra z komputerem, przez sieć oraz powrót"
        else:
            data["action"] = "error"
            data["errorMessage"] = "Nieprawidłowa opcja"
    else:
        data["action"] = "none"
    return data

def get_settings_action():
    data = {}
    text = listen()
    if(text):
        text = text.replace(" ","").lower()
        if(re.search("(poziom|trud|moc|pc|komputer)", text)):
            text = replacer(text, level_dict)
            try:
                match = re.search("[1-8]", text)
                if match:
                    data["level"] = match.group(0)
                    data["action"] = "engine"
                else:
                    data["action"] = "error"
                    data["errorMessage"] = "Nieprawidłowy poziom trudności"
            except Exception as ex:
                print("get_settings_action failed:", ex)
                data["action"] = "error"
                data["errorMessage"] = "Nieprawidłowa wartość"

        elif(re.search("(kolor|strona|figur)", text)):
            try:
                if(re.search("(biał)", text)):
                    data["piecesColor"] = "white"
                    data["action"] = "piecesColor"
                elif(re.search("(czarn)", text)):
                    data["piecesColor"] = "black"
                    data["action"] = "piecesColor"
                elif(re.search("(los)", text)):
                    data["piecesColor"] = "random"
                    data["action"] = "piecesColor"
                else:
                    data["action"] = "error"
                    data["errorMessage"] = "Nieprawidłowa opcja"
            except Exception as ex:
                print("get_settings_action failed:", ex)
                data["action"] = "error"
                data["errorMessage"] = "Nieprawidłowa wartość"

        elif(re.search("(mikro|dźwi|akty)", text)):
            try:
                if(re.search("(wł)", text)):
                    data["activeMicSound"] = "on"
                    data["action"] = "activeMicSound"
                elif(re.search("(wył)", text)):
                    data["activeMicSound"] = "off"
                    data["action"] = "activeMicSound"
                else:
                    data["action"] = "error"
                    data["errorMessage"] = "Nieprawidłowa opcja"
            except Exception as ex:
                print("get_settings_action failed:", ex)
                data["action"] = "error"
                data["errorMessage"] = "Nieprawidłowa wartość"

        elif(re.search("(komun|głos|okna)", text)):
            try:
                if(re.search("(wł)", text)):
                    data["pageSound"] = "on"
                    data["action"] = "pageSound"
                elif(re.search("(wył)", text)):
                    data["pageSound"] = "off"
                    data["action"] = "pageSound"
                else:
                    data["action"] = "error"
                    data["errorMessage"] = "Nieprawidłowa opcja"
            except Exception as ex:
                print("get_settings_action failed:", ex)
                data["action"] = "error"
                data["errorMessage"] = "Nieprawidłowa wartość"

        elif(re.search("(pomoc|instrukcj|corobić|jak|pomóż)", text)):
            data["action"] = "help"
           
        elif(re.search("(powr|wró|zamkn)", text)):
            data["action"] = "return"
            
        elif(re.search("(zapis)", text)):
            data["action"] = "save"

        else:
            data["action"] = "error"
            data["errorMessage"] = "Nieprawidłowa opcja"
    else:
        data["action"] = "none"
    return data

def get_wait_action():
    data = {}
    text = listen()
    if text:
        text = text.replace(" ","").lower()
        if(re.search("(wyjście|zakończ|zamknij|wyjdź|powrót|wróc)", text)):
            data["action"] = "return"
        else:
            print(text)
            data["action"] = "error"
            data["errorMessage"] = "Niepoprawna akcja"
    else:
        data["action"] = "none"
    return data

def get_player_action():
    data = {}
    text = listen()
    if text:
        text = text.replace(" ","").lower()
        if re.search("poddaj", text):
            data["action"] = "surrender"
        elif (re.search("pole", text)):
            text = text.replace("pole","")
            match = re.search("[a-h][1-8]", text)
            data["action"] = "checkField"
            if(match):
                data["field"] = match.group(0)
            else:
                data["field"] = "badfield"
        else:
            text = replacer(text, player_move_dict)
            if(len(text)<6 and re.search("[a-h][1-8]|O-O", text)): 
                data["action"] = "move"
                data["move"] = text
            else:
                print(text)
                data["action"] = "error"
                # data["errorMessage"] = "Niepoprawna akcja"
    else:
        data["action"] = "none"
    return data

#======================== Output audio functions =============================

def sayWords(text):
    converter = pyttsx3.init()
    converter.stop()
    converter.setProperty('rate', 140) 
    converter.setProperty('volume', 1)
    converter.say(text)
    try:
        converter.runAndWait() 
    except Exception as ex:
        print("Error: ", ex)

def sayPiece(field, color, type):
    text = field
    figury = ("pionek", "skoczek", "goniec", "wieża", "hetman", "król")
    if(color):
        if(type == 4):
            text += "biała "
        else:
            text += "biały "
    else:
        if(type == 4):
            text += "czarna "
        else:
            text += "czarny "
    text += figury[type-1]
    sayWords(text)

def sayMove(text):
    text = replacer(text, move_dict)
    sayWords(text)