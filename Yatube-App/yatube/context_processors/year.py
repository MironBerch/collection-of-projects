import datetime


def year(request):
    """Fuction for displayed year"""
    year = datetime.datetime.now().year
    context = {'year': year}
    return context