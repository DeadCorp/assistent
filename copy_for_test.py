from __future__ import print_function
import datetime
import os.path
import pyaudio
import os
import time
import pyttsx3
import speech_recognition as sr
import pytz
import subprocess
import pickle
import requests
import json

#write this commands to files

# COMMAND = {
#     'wake' : ['jarvis','джарвис'],
#     'close_programm' : ['bay','close','bay bay','sleep','time to sleep','выключайся','пока','закончи роботу','спи'],
#     'note' : ["make a note", "write this down", "remember this",'запиши это','запомни','сохрани','запиши'],
#     'yes' : ['ok','okey','yes','yea','да','ок','окей'],
#     'not' : ['no','not','нет','не'],
#     'language' : ['сменим','изменть','смени','измени','change','language','pick language'],
#     'launch' : ['start','launch','open','открой','запусти'],
#     'add instruction' : ['добавить команду','add command'],
#     'add game' : ['add game','добавить игру'],
# }

# GAME = {    
#     'dota2' : ['dota','dota2','dota 2','defens of the ancient 2','defens of the ancient','доту','дота',570],
#     'witcher3' : ['witcher','witcher 3','the witcher','best game','gwin blade','ведьмак','ведьмака','ведьмак 3','белого волка',292030],
# }


#   Запускається якщо неможе найти або открити файл з ід игр стим
def update_steam_games():
    i = requests.get('http://api.steampowered.com/ISteamApps/GetAppList/v0002/')
    if i.status_code == 200:
        with open(r'./commands/ids','wb') as target:
            pickle.dump(i.text,target)
    else:
        update_steam_games()

#   Передаєм назву гри , шукаємо її в стімі, та вертаємо ід гри
#   якщо неможемо відкрити файл з ід ігр, запускається метод update_steam_games()
def get_game_id(name):
    
    id = 0
    try:
        with open(r'./commands/ids','rb') as target:
            s = json.loads(pickle.load(target))

        for app in s['applist']['apps']: 
            if app['name'].lower() == name.lower():
                id = app['appid']
                print(app['name'] + '   ' + str(app['appid']))

        return id
    except:
        update_steam_games()
        get_game_id(name)

#   Витягуємо з файлу команди для роботи з ними.
#   команди за допомогою бібліотеки pickle записуються 
#   та витягуються з файлу
def get_command(filename):
    s = open(r'./commands/'+filename,'rb')
    dict_commands = {}
    # with open('pickle-first.txt', 'wb') as f:
    #     pickle.dump(COMMAND, f)
 
    with s as f:
        dict_commands = pickle.load(f)
    s.close()

    return dict_commands

#   Записуємо команди в файл
def set_command(filename,command_dict):
    s = open(r'./commands/'+filename,'wb')
    with s as f:
        pickle.dump(command_dict, f) 
    s.close()
   
#   Відтворення тексту
def speak(text):    
    engine.say(text)
    engine.runAndWait()

#   language = 'en-US' 
#   Прослуховування тексту
def get_audio(asd = 'dodi'):
    if asd == "idod":
        asd = 'en-US'
    else:
        asd = language
    

    r = sr.Recognizer()   

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=0.3)
        audio = r.listen(source)
        said = ""
        
        try:
            said = r.recognize_google(audio,language=asd)
            print(said)
        except :
            print("Exception: " )
             
    return said.lower()

#   Запис нотатки
def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name])

#   Запис нотатки
def set(text):
    copy = text
    new_text = copy.replace(phrase,'')
    speak_lan("хочешь записать что нибуть еще?",'you want to add something else')
    question = get_audio()    
    if question in commands['yes']:
        speak_lan('диктуй','write what')
        note_text = get_audio()
        write = new_text + ' ' + note_text
        note(write)
    
    else :
        note(new_text)
    speak_lan("Я записал",'I am write this down')

#   Виключення програми
def bay():
    for s in commands['close_programm']:
        if s in text:
            speak('Пока :>)')
            os.abort()

#   Відтворення фрази в залежності від обраної мови
def speak_lan(phrase_ru,phrase_en):
    if language == 'ru':
        speak(phrase_ru)
    elif language == 'en-US':
        speak(phrase_en)

#   Ініціалізація мікро, встановлення голосу
def init():
    engine = pyttsx3.init()
    voice = engine.getProperty("voices")
    for v in voice:
        if v.name == "Alyona (Russian) SAPI5":
            engine.setProperty("voice", v.id)
    return engine

#   Зміна мови
def change_language(language,spe = True):
    if language == 'ru':
        save_language('en-US')

    elif language == 'en-US':
        save_language('ru')

    if spe == True:
        speak_lan('Язык был изменен','language has be chenged')
    return True 
#   Зчитування мови
def read_language():
    with open(r'./commands/language.txt','r+') as p:
        s = p.read()
    return s

#   Зміна мови
def save_language(text):
    with open(r'./commands/language.txt','w+') as p:        
        p.write(text)

#   Додавання гри до файлу зі списком ігр.
#   Для запуску гри використовується стім ід гри
#   стім ід повинен бути записаний останній після усіх можливих назв гри.
#   Стім айді повинен записатися автоматично якщо знайде назву гри у списку ігр стім (файл - ids)
def add_game():
    speak_lan('какую игру нужно добавить, название должно быть как можно точнее на агнлийском','what game you want to add, need the exact name')
    
    game_name = get_audio(asd='idod')
    
    game_id = 0

    game_id = get_game_id(game_name)

    copy_games =games

    if game_name in copy_games:
        copy_games[game_name].remove(copy_games[game_name][-1])
        copy_games[game_name].append('')
    else:
        copy_games[game_name] = ['']

    speak_lan('нужно добавить кулючевые слова  для запуска игры','need add key word  for start the game')
    speak_lan('чтобы закончить додавание слов, произнесите "хватит"','for end add wordjust say "enough"')

    while True:
        speak_lan('назовите слово','say word')
        value = get_audio()
        if value == 'хватит' or value == 'enough': 

            copy_games[game_name].remove('')
            copy_games[game_name].append(game_id)
            break
        else:
            copy_games[game_name].append(value)

    set_command('games.txt',copy_games)
    speak_lan('спасибо, игры были добавлены','thaks, games added')
    return True

#   Додавання команди до списку команд
#   Команда має ідентифікатор(ключ) та ключові слова для її виклику
#   Для будь якої існуючої команди можна додати ключові слова за допомогою цього методу.
#   Щоб це зробити потрібно назвати існуючий у файлі ідентифікатор
#
#   Увага
#   За допомогою цього методу можна лише добавити команду в файл
#   щоб користуватися командою необхідно описати її логіку в коді
#   также як і для інших команд
#
#   if ідентифікатор(ключ) in commands: #дуже важлива перевірка, без неї програма не працюватиме
#       for phrase in commands[ідентифікатор(ключ)]:
#           if phrase in text:
#               pass
def add_command():
    speak_lan('нужно добавить идентификатор  для команды на английском','need identificator  for command')
    say_key = get_audio(asd='idod')
    copy_commands = commands
    if say_key in copy_commands:
        copy_commands[say_key].append('')
    else:
        copy_commands[say_key] = ['']
    speak_lan('нужно добавить кулючевые слова  для команды','need add key word  for command')
    speak_lan('чтобы закончить додавание слов, произнесите "хватит"','for end add wordjust say "enough"')

    a_bool = True
    while a_bool == True:
        speak_lan('назовите слово','say word')
        say_value = get_audio()
        if say_value == 'хватит' or say_value == 'enough': 
            copy_commands[say_key].remove('')
            break
        else:
            copy_commands[say_key].append(say_value)

    set_command('command.txt',copy_commands)
    speak_lan('спасибо, команды были добавлены','thaks, command added')
    return True

#   Запуск гри зі стім
def run_game(game):
    id = 0
    for i in games:
        for game_name in games[i]:
            if str(game_name) in game:
                id = games[i][-1]
                subprocess.run("start steam://rungameid/" + str(id), shell=True)

#   Обробник для фрази у якій команда йде разом з словом - звертанням до програми
def is_command_in_wake(text,say):
    temp = text[text.find(say) : ]
    if temp == say:
        speak_lan('Слушаю','I am ready')            
        text = get_audio()
    else:
        speak_lan('Слушаю','I am ready')          
        text = temp.replace(say+' ','')
        
        for i in commands:
            for s in commands[i]:
                if s in text:                    
                    return text
        
        text = get_audio()
    return  text




#   Запуск програми

print("Start")
engine =  init()

#   Вібір мови, її можна змінити під час роботи програми
language = read_language()

#   Змінні - прапори
check_for_update_command = False
check_for_language_change = False

#   Загрузка списків команд та ігор
commands = get_command('command.txt')
games = get_command('games.txt')

print(commands)
print(games)


#   Бескінечний цикл, для виходу треба попрощатись з помічником



while True:

    #   Перевірка чи не змінились команди та ігри  і їх перезагрузка, якщо змінилися
    if check_for_update_command == True:
        commands = get_command('command.txt')
        games = get_command('games.txt')
        check_for_update_command = False

    #   Перевірка чи незмінилася мова
    if check_for_language_change == True:
        language = read_language()
        check_for_language_change = False

    print("Listening")

    #   Прослуховування мікрофону
    text = get_audio()

    #   Перевірка почутої фрази
    if text != '':
        for say in commands['wake']:        
            if say in text:

                #   Перевірка чи є команда в зверненні
                text = is_command_in_wake(text,say)                  
            
                
                #   Записати що небуть
                if 'note' in commands:
                    for phrase in commands['note']:
                        if phrase in text:
                            set(text)
                
                
                #   Запустити гру
                if 'launch' in commands:
                    for phrase in commands['launch']:
                        if phrase == text:
                            speak_lan('Что запустить','launch what')
                            game = get_audio()
                            run_game(game)
                        elif phrase in text:
                            run_game(text)

                #   Змінити мову
                if 'language' in commands:
                    for phrase in commands['language']:
                        if phrase in text:
                            check_for_language_change =  change_language(language)
                            break   

                #   Анекдот
                if 'анекдот' in commands:
                    for phrase in commands['анекдот']:
                        if phrase in text:
                            speak('Шутка хахахахах')

                #   Додавання команд
                if 'add instruction' in commands: 
                    for phrase in commands['add instruction']:
                        if phrase in text:
                            check_for_update_command = add_command()
                

                #   Додавання ігор
                if 'add game' in commands or 'добавить игру' in commands:
                    for phrase in commands['add game']:
                        if phrase in text:
                            check_for_update_command = add_game()


                bay()     
        else:
            bay()
    else:
        continue    