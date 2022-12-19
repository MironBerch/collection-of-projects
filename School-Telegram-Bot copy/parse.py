async def message_parse(data):
    year_study = data['scholl_class'][0:-1].lower()
    class_letter = data['scholl_class'][-1].lower()

    context = {
        'class_letter': class_letter,
        'year_study': year_study
    }
    
    return context