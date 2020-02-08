from __future__ import print_function
import datetime
import pickle
import os.path
import os
import time
import pyttsx3
import speech_recognition as sr
import pytz
import subprocess

WAKE = ["jarvis",'джарвис']
SLEEP = ['bay','close','bay bay','sleep','time to sleep','выключайся','пока','закончи роботу','спи']
NOTE_STRS = ["make a note", "write this down", "remember this",'запиши это','запомни','сохрани','запиши']
YES = ['ok','okey','hey','yes','yea','да','запиши','хочу']
NO = ['no','нет','не хочу']
LAN_CHANGE = ['сменим','изменть','смени','измени','change','language','pick language']

def speak(text):    
    engine.say(text)
    engine.runAndWait()

#language = 'en-US'
def get_audio(language = 'ru'):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""
        
        try:
            said = r.recognize_google(audio,language=language)
            print(said)
        except :
            print("Exception: " )

    return said.lower()

def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name])

def set(text):
    copy = text
    new_text = copy.replace(phrase,'')
    speak_lan("хочешь записать что нибуть еще?",'you want to add something else')
    question = get_audio(language)    
    if question in YES:
        speak_lan('диктуй','write what')
        note_text = get_audio(language)
        write = new_text + ' ' + note_text
        note(write)
    elif question in NO:
        note(new_text)
    else :
        note(new_text)
    speak_lan("Я записал",'I am write this down')

def bay():
    for s in SLEEP:
        if s in text:
            speak('Пока :>)')
            os.abort()

def speak_lan(phrase_ru,phrase_en):
    if language == 'ru':
        speak(phrase_ru)
    elif language == 'en-US':
        speak(phrase_en)

def init():
    engine = pyttsx3.init()
    voice = engine.getProperty("voices")
    for v in voice:
        if v.name == "Alyona (Russian) SAPI5":
            engine.setProperty("voice", v.id)
    return engine


print("Start")
engine =  init()
language = 'ru'

while True:

    
    print("Listening")
    text = get_audio(language)
    for say in WAKE:        
        if say in text:
            speak_lan('Да, хазззяин','I am ready')            
            text = get_audio(language)
            
            for phrase in NOTE_STRS:
                if phrase in text:
                    set(text)
            
            bay()

            for phrase in LAN_CHANGE:
                if phrase in text:
                    if language == 'ru':
                        language = 'en-US'
                        
                    elif language == 'en-US':
                        language = 'ru'
                        
                    speak_lan('Язык был изменен','language has be chenged')
                    break        
    else:
        bay()

    