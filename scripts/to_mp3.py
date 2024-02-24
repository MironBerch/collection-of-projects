from gtts import gTTS


def read_text_from_file(file_name: str):
    with open(f'answers/{file_name}.md') as file:
        text = file.readlines()
        read_result: list[str] = []
        for string in text:
            while '*' in string or '`' in string:
                string = string.replace('*', '', 1)
                string = string.replace('`', '', 1)
                string = string.replace('__', ' (два нижних подчёркивания) ', 1)
            read_result.append(string)
        return ' '.join(read_result)


def text_to_mp3(text: str, file_name: str):
    myobj = gTTS(text=text, lang='ru', slow=False)
    myobj.save(f'mp3s/{file_name}.mp3')


with open('res.txt') as file:
    for file_name in file.readlines():
        file_name = file_name.replace('\n', '', 1)
        try:
            text_to_mp3(
                text=read_text_from_file(file_name=file_name),
                file_name=file_name,
            )
        except Exception as e:
            print(f'неудача: {file_name}')
            print(e)
        else:
            print(f'успех: {file_name}')
