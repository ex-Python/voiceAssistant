# Голосовой ассистент КЕША 1.0 BETA
import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import random
import webbrowser

# настройки
opts = {
    "alias": ('луна','люна','уна','луно'),
    "tbr": ('скажи','расскажи','покажи','сколько','произнеси'),
    "cmds": {
        "ctime": ('текущее время','сейчас времени','который час'),
        "radio": ('включи музыку','воспроизведи радио','включи радио'),
        "stupid1": ('расскажи анекдот','рассмеши меня','ты знаешь анекдоты'),
        "open_ggl": ('открой гугл','открой google'),
        "off": ('выключи компьютер','завершение работы'),
        "youtube": ('включи ютуб','открой ютуб','открой youtube','включи youtube'),
        "whatsapp": ('открой ватсап','открой whatsapp')
    }
}
 
# функции
def speak(what):
    print( what )
    speak_engine.say( what )
    speak_engine.runAndWait()
    speak_engine.stop()
 
def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language = "ru-RU").lower()
        print("[log] Распознано: " + voice)
   
        if voice.startswith(opts["alias"]):
            # обращаются к Кеше
            cmd = voice
 
            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()
           
            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()
           
            # распознаем и выполняем команду
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])
 
    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")
 
def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c,v in opts['cmds'].items():
 
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
   
    return RC
 
def execute_cmd(cmd):
    if cmd == 'ctime':
        # сказать текущее время
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))
   
    elif cmd == 'radio':
        # воспроизвести радио
        os.startfile("C:\\Program Files (x86)\\PCRadio\\PCRadio.exe")
   
    elif cmd == 'stupid1':
        # рассказать анекдот
        selectanekdot = ["У меня была одна проблема, поэтому я решил написать программу, которая её решит. Теперь у меня есть 1 проблема, 9 ошибок и 12 предупреждений.", "Такое ощущение, что между первой волной коронавируса и второй, будет всего 1 день - день голосования по поправкам в Конституцию.","Электронное голосование в России - это как в фильме Матрица, только на выбор будет две таблетки одного цвета."]
        speak(random.choice(selectanekdot))

    elif cmd == 'open_ggl':
        # открыть гугл
        os.startfile("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe")

    elif cmd == 'youtube':
		#открыть ютуб
	    webbrowser.get(using='C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe').open_new_tab('https://www.youtube.com/?gl=RU&hl=ru')

    elif cmd == 'off':
		#выключить компьютер
    	global quit
    	os.system('shutdown /s /f /t 10')
    	quit()

    else:
        print('Команда не распознана, повторите!')
 
# запуск
r = sr.Recognizer()
m = sr.Microphone(device_index = 1)
 
with m as source:
    r.adjust_for_ambient_noise(source)
 
speak_engine = pyttsx3.init()
 
# Только если у вас установлены голоса для синтеза речи!
voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voice', voices[0].id)
 
# forced cmd test 
speak_hello = ["Здравствуйте",]
speak("Луна слушает")
 
stop_listening = r.listen_in_background(m, callback)
while True: time.sleep(0.1) # infinity loop
