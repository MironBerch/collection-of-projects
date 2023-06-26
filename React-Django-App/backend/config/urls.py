from django.urls import path

from api.views import PostView

urlpatterns = [
    path('', PostView.as_view())
]
