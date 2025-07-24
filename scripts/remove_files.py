import os

files = os.listdir('answers/')
edit_lines = []
with open('вопросы.md') as f:
    lines = f.readlines()
    for line in lines:
        line = line.split('[[')[-1]
        line = line.split(']]')[0]
        edit_lines.append(f'{line}.md')

for file in files:
    if file not in edit_lines:
        os.remove(f'answers/{file}')
        print(file)
