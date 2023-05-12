from django.shortcuts import render


def bad_request_view(request, *args, **kwargs):
    response = render(request, 'misc/400.html')
    response.status_code = 400
    return response


def permission_denied_view(request, *args, **kwargs):
    response = render(request, 'misc/403.html')
    response.status_code = 403
    return response


def page_not_found_view(request, *args, **kwargs):
    response = render(request, 'misc/404.html')
    response.status_code = 404
    return response


def server_error_view(request, *args, **kwargs):
    response = render(request, 'misc/500.html')
    response.status_code = 500
    return response
