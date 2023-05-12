from reporting.models import Contest


def get_contest(id: int):
    """return contest by id"""
    contest = Contest.objects.get(id=id)
    return contest


def get_all_contests():
    """return all contests"""
    contests = Contest.objects.all().order_by('-id')
    return contests


def get_users_creation_contests(user):
    """return contests which created by user"""
    contests = Contest.objects.filter(
        contest_creater=user,
    ).order_by('-id')
    return contests
