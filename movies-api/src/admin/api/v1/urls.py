from django.urls import include, path

app_name = 'api'

urlpatterns = [
    path('schema/', include('api.v1.schema.urls')),

    path('movies/', include('api.v1.movies.urls')),
]
