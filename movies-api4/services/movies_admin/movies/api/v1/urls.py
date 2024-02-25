from django.urls import include, path

app_name = 'api'

urlpatterns = [
    path('schema/', include('movies.api.v1.schema.urls')),

    path('movies/', include('movies.api.v1.movies.urls')),
]
