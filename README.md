# Приложение для транскрипции речи из видеофайлов - ЕВГЕНИЧ.ИИ

Это приложение позволяет загружать видеофайлы с Яндекс.Диска, преобразовывать их в аудиофайлы и транскрибировать речь в текст. Проект предоставляет выбор между двумя моделями для распознавания речи: Wav2Vec2 от Hugging Face и Vosk для оффлайн-распознавания.

## Основные компоненты

### Файлы с кодом

- **`download_video`** — функция для загрузки видеофайла с Яндекс.Диска по предоставленной ссылке.
  
- **`convert_video_to_audio`** — функция для конвертации видеофайла в аудиоформат WAV с использованием `ffmpeg`. Аудио сохраняется с частотой дискретизации 16 кГц, что подходит для использования с моделями распознавания речи.

- **`transcribe_with_wav2vec2`** — функция для транскрипции аудио в текст с использованием модели Wav2Vec2 от Hugging Face, которая работает в онлайн-режиме. Подходит для распознавания речи на русском языке.

- **`transcribe_with_vosk`** — функция для транскрипции аудио с использованием оффлайн-модели Vosk. Требует предварительной загрузки модели и подходит для случаев, когда интернет-соединение ограничено или недоступно.

- **`transcribe_video`** — основная функция, объединяющая загрузку видео, его конвертацию в аудио и последующую транскрипцию. Предоставляет выбор модели для распознавания речи (`wav2vec2` или `vosk`).

### Остальные файлы

- **`requirements.txt`** — список зависимостей, необходимых для локального запуска приложения.

## Требования к окружению

- **Python 3.7+**
- **ffmpeg** — для установки ffmpeg выполните следующие команды:
  - **Ubuntu**:
    ```bash
    sudo apt update
    sudo apt install ffmpeg
    ```
  - **Windows**: Загрузите `ffmpeg` с [официального сайта](https://ffmpeg.org/download.html) и добавьте его в переменную окружения `PATH`.

- **Библиотеки Python** — установите необходимые библиотеки с помощью команды:
  ```bash
  pip install -r requirements.txt
