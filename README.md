# AudioChess

## Table of contents
* [About](#about)
* [Used Technologies](#technologies)
* [How to Setup](#setup)

## About
AudioChess is simple python game, where You can play chess and control whole app using voice commands in polish. It is an engineering thesis project written to learn python.
	
## Technologies
Project is created with:
* Python: 3.6.8
* PyQt: 5.15.2
* Microsoft Speech API (SAPI): 5.3

## Libraries
This project use fallowing python libraries: 
* chess: 1.5.0
* pyttsx3: 2.90 
* playsound: 1.2.2 
* SpeechRecognition: 3.8.1
	
## Requirements
For the app to work properly, the requirements must be met:
* Windows 10 with SAPI
* Working microphone and speakers (or headset)


## Setup
To run this project, install requirements from file,

```
pip3 install -r requirements.txt
```
And then run app from main file
```
python main.py
```
Or run AudioChess.exe

## Improvements

Multiplayer game is available after starting server.py but only locally.
Next step would be to get real online mode.
Also adding english langueage.