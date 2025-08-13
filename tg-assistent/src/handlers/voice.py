import os
from telegram import Update
from telegram.ext import  ContextTypes
import speech_recognition as sr
from pydub import AudioSegment

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message or not update.message.voice:
            return

        voice = update.message.voice
        bot = context.bot
        
        # Получаем файл
        file = await bot.get_file(voice.file_id)
        
        # Создаем временную папку
        os.makedirs("temp_voice", exist_ok=True)
        file_id = voice.file_unique_id
        ogg_path = f"temp_voice/{file_id}.ogg"
        wav_path = f"temp_voice/{file_id}.wav"
        
        # Скачиваем и конвертируем
        await file.download_to_drive(ogg_path)
        AudioSegment.from_ogg(ogg_path).export(wav_path, format="wav")
        
        # Распознаем речь
        r = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio = r.record(source)
            try:
                text = r.recognize_google(audio, language="ru-RU")
                await update.message.reply_text(f"🎤 Распознано: {text}")
            except sr.UnknownValueError:
                await update.message.reply_text("❌ Речь не распознана")
            except sr.RequestError as e:
                await update.message.reply_text(f"❌ Ошибка сервиса: {e}")
        
    except Exception as e:
        await update.message.reply_text(f"⚠️ Произошла ошибка при обработке {e}")
        
    finally:
        # Очистка временных файлов
        for path in [ogg_path, wav_path]:
            try:
                if path and os.path.exists(path):
                    os.remove(path)
            except Exception as e:
                ...
