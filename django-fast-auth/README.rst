Django-Fast-Auth

Fast-Auth is a fast simple registration Django application.

Detailed documentation is in the "docs" directory.

Fast start
-----------

1. Add "fast_auth" to your INSTALLED_APPS settings as follows:

```
    INSTALLED_APPS = [
        ...
        'fast_auth',
    ]
```

2. Add some constants to your settings:

```
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'fast_auth.email_backend.CustomBackend',
]
```

```
LOGIN_REDIRECT_URL = "/"
```
3. Include URLconf polls in your urls.py project as follows:

```
    path('auth/', include('fast_auth.urls')),
```

4. Visit http://127.0.0.1:8000/auth/ to to register.