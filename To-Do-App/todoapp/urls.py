from django.urls import path
from .views import TaskList, TaskCreate, TaskUpdate, TaskDelete, LoginView, RegisterPage
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', TaskList.as_view(), name='home'),
    path('create-task/', TaskCreate.as_view(), name='create-task'),
    path('update-task/<int:pk>/', TaskUpdate.as_view(), name='update-task'),
    path('delete-task/<int:pk>/', TaskDelete.as_view(), name='delete-task'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
]