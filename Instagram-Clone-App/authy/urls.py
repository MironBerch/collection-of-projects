from django.urls import path
from authy.views import signup, edit_profile
from django.contrib.auth import views as authViews 


urlpatterns = [
    path('profile/edit', edit_profile, name='edit-profile'),
   	path('signup/', signup, name='signup'),
   	path('login/', authViews.LoginView.as_view(template_name='authy/login.html'), name='login'),
   	path('logout/', authViews.LogoutView.as_view(), {'next_page' : 'index'}, name='logout'),
]