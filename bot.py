import os
import requests
import subprocess
import torch
import soundfile as sf
import wave
import json
from vosk import Model as VoskModel, KaldiRecognizer
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

# Функция для загрузки видео с Яндекс.Диска
def download_video(url, output_path="video.mp4"):
    """
    Скачивает видеофайл по указанному URL и сохраняет его в output_path.
    """
    response = requests.get(url)
    with open(output_path, "wb") as f:
        f.write(response.content)
    print("Видео скачано:", output_path)

# Функция для конвертации видео в аудио
def convert_video_to_audio(video_path="video.mp4", audio_path="audio.wav"):
    """
    Преобразует видеофайл в аудиоформат (WAV) с помощью ffmpeg.
    Параметры: 
      - video_path: путь к исходному видеофайлу.
      - audio_path: путь для сохранения преобразованного аудиофайла.
    """
    command = f"ffmpeg -i {video_path} -ac 1 -ar 16000 {audio_path}"
    subprocess.run(command, shell=True)
    print("Аудио файл создан:", audio_path)

# Функция транскрипции аудио в текст с помощью Wav2Vec2
def transcribe_with_wav2vec2(audio_path="audio.wav"):
    """
    Транскрибирует аудиофайл в текст с использованием модели Wav2Vec2.
    Параметры: 
      - audio_path: путь к аудиофайлу.
    Возвращает: строку с расшифровкой текста.
    """
    # Загрузим предобученные процессор и модель Wav2Vec2
    processor = Wav2Vec2Processor.from_pretrained("jonatasgrosman/wav2vec2-large-xlsr-53-russian")
    model = Wav2Vec2ForCTC.from_pretrained("jonatasgrosman/wav2vec2-large-xlsr-53-russian")

    # Загружаем аудиофайл и подготавливаем его для модели
    audio_input, sample_rate = sf.read(audio_path)
    input_values = processor(audio_input, sampling_rate=sample_rate, return_tensors="pt").input_values

    # Получаем логиты (предсказания модели) и выбираем наиболее вероятные значения
    with torch.no_grad():
        logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)

    # Декодируем предсказанные индексы в текст
    transcription = processor.decode(predicted_ids[0])
    return transcription

# Функция транскрипции аудио в текст с помощью Vosk
def transcribe_with_vosk(audio_path="audio.wav"):
    """
    Транскрибирует аудиофайл в текст с использованием модели Vosk.
    Параметры:
      - audio_path: путь к аудиофайлу.
    Возвращает: строку с расшифровкой текста.
    """
    # Проверяем, установлена ли модель для Vosk
    if not os.path.exists("model"):
        print("Скачайте русскую модель для Vosk с https://alphacephei.com/vosk/models и распакуйте её в папку 'model'")
        return

    # Загружаем модель Vosk и создаём объект распознавателя
    model = VoskModel("model")
    recognizer = KaldiRecognizer(model, 16000)

    # Открываем аудиофайл и передаём данные для распознавания
    with wave.open(audio_path, "rb") as wf:
        results = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            # Если фрагмент распознан, добавляем результат в список
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                results.append(result['text'])
        # Обрабатываем финальный результат
        final_result = json.loads(recognizer.FinalResult())
        results.append(final_result['text'])

    # Объединяем все результаты в одну строку
    transcription = " ".join(results)
    return transcription

# Основная функция, объединяющая все шаги
def transcribe_video(url, use_model="wav2vec2"):
    """
    Скачивает видео, конвертирует его в аудио, а затем транскрибирует с использованием выбранной модели.
    Параметры:
      - url: ссылка на видеофайл на Яндекс.Диске.
      - use_model: 'wav2vec2' для использования Wav2Vec2 или 'vosk' для использования Vosk.
    """
    # Шаг 1: Скачиваем видео
    download_video(url)
    
    # Шаг 2: Конвертируем видео в аудио
    convert_video_to_audio()

    # Шаг 3: Транскрибируем аудио в текст
    if use_model == "wav2vec2":
        transcription = transcribe_with_wav2vec2()
    elif use_model == "vosk":
        transcription = transcribe_with_vosk()
    else:
        raise ValueError("Неправильное значение для use_model. Используйте 'wav2vec2' или 'vosk'.")

    print("Транскрипция текста:", transcription)

# Пример использования
url = "Ваша_ссылка_на_скачивание_с_Яндекс.Диска"
transcribe_video(url, use_model="wav2vec2")  # Или "vosk" для использования модели Vosk
