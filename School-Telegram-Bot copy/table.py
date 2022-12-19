async def create_answer(xlsx):
    subjects = xlsx[0]
    rooms = xlsx[-1]
    answer = ['Расписание:\n']
    days = ['\nПонедельник:\n', '\nВторник:\n', '\nСреда:\n', '\nЧетверг:\n', '\nПятница:\n', '\nСубота:\n',]
    day = 0
    start_day_index = [0, 7, 14, 21, 28, 35]

    for object in range(len(subjects)):
        if object in start_day_index:
            answer.append(days[day])
            day+=1
        answer.append(str(subjects[object]))
        answer.append(' - ')
        answer.append(str(rooms[object]))
        answer.append('\n')

    s = ''.join(answer)
    
    return s