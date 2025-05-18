import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import random

duration = 5  # секунды записи
sample_rate = 44100

words_by_level = {
    "easy": ["кот", "собака", "яблоко", "молоко", "солнце"],
    "medium": ["банан", "школа", "друг", "окно", "жёлтый"],
    "hard": ["технология", "университет", "информация", "произношение", "воображение"]
}

level_choose = ('Хочешь проверить свое произношение английских слов? Выбери уровень сложности!\n'
                '1. Легкий (easy)\n'
                '2. Средний (medium)\n'
                '3. Сложный (hard)\n'
                'Введите номер уровня: ')

while True:
    level_number = input(level_choose)
    if level_number == '1':
        level = "easy"
        break
    elif level_number == '2':
        level = "medium"
        break
    elif level_number == '3':
        level = "hard"
        break
    else:
        print("Некорректный ввод. Пожалуйста, выберите 1, 2 или 3.")

chosen_word = random.choice(words_by_level[level])
print(f'Хорошо! Вот слово для произношения: {chosen_word}')

balls = 0
mistakes = 0

while mistakes < 3:
    print("🎙 Говори...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
    sd.wait()
    wav.write("output.wav", sample_rate, recording)
    print("✅ Запись завершена, теперь распознаём...")

    recognizer = sr.Recognizer()
    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language="en-EN")
        print("📝 Ты сказал:", text)
        

        # Перевод текста
        translator = Translator()
        # lang = input("На какой язык перевести? (например, 'en' — английский, 'es' — испанский): ")
        # translated = translator.translate(text, dest=lang)
        # print(f"🌍 Перевод на {lang}:", translated.text)
        translated_to_russian = translator.translate(text, dest='ru').text
        print(f"🌍 Перевод на русский:", translated_to_russian)


        if translated_to_russian.lower() == chosen_word.lower():
            balls += 1
            print(f'Молодец! Ты правильно сказал слово. Твои баллы: {balls}')
            chosen_word = random.choice(words_by_level[level])
            print(f'Хорошо! Вот слово для произношения: {chosen_word}')
        else:
            mistakes += 1
            print(f'О нет! Ты ошибся :( Вот количество твоих ошибок: {mistakes})')
            chosen_word = random.choice(words_by_level[level])
            print(f'Хорошо! Вот слово для произношения: {chosen_word}')

    except sr.UnknownValueError:
        print("😕 Не удалось распознать речь.")
    except sr.RequestError as e:
        print(f"❗️ Ошибка сервиса: {e}")

if mistakes == 3:
    print('Ты запорол игру, ботяра!😹 Учи английский!')
      
