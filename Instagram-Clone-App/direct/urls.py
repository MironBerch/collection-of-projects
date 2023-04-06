from django.urls import path
from .views import inbox, user_search, directs, new_conversation, send_direct


urlpatterns = [
    path('', inbox, name='inbox'),
    path('directors/<username>', directs, name='directs'),
    path('new/', user_search, name='usersearch'),
    path('new/<username>', new_conversation, name='newconversation'),
    path('send/', send_direct, name='send_direct'),
]