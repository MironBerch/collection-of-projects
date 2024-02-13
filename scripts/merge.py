import os
import subprocess

# Создаем временную папку для обработки
os.makedirs('temp_processed', exist_ok=True)

# Создаем файл с тишиной (10 секунд)
subprocess.run([
    'ffmpeg',
    '-f', 'lavfi',
    '-i', 'anullsrc=r=44100:cl=stereo',
    '-t', '10',
    '-acodec', 'libmp3lame',
    'temp_processed/silence_10s.mp3'
])

# Обрабатываем каждый MP3-файл
processed_files = []
for i, filename in enumerate(sorted(os.listdir('mp3s/'))):
    if not filename.endswith('.mp3'):
        continue
        
    input_path = os.path.join('mp3s', filename)
    output_path = os.path.join('temp_processed', f'processed_{i}.mp3')
    
    # Ускоряем аудио в 2x и конвертируем в единый формат
    subprocess.run([
        'ffmpeg',
        '-i', input_path,
        '-filter:a', 'atempo=1.5',
        '-ar', '44100',
        '-ac', '2',
        '-b:a', '192k',
        output_path
    ])
    processed_files.append(output_path)

# Создаем список для конкатенации
with open('concat_list.txt', 'w') as f:
    for i, file_path in enumerate(processed_files):
        f.write(f"file '{file_path}'\n")
        if i < len(processed_files) - 1:
            f.write(f"file 'temp_processed/silence_10s.mp3'\n")

# Объединяем все файлы
subprocess.run([
    'ffmpeg',
    '-f', 'concat',
    '-safe', '0',
    '-i', 'concat_list.txt',
    '-c', 'copy',
    'combined_result.mp3'
])

# Очистка временных файлов (раскомментировать при необходимости)
# import shutil
# shutil.rmtree('temp_processed')
# os.remove('concat_list.txt')

print("Объединение завершено! Результат в combined_result.mp3")
