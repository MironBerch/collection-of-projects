from django.urls import path
from api.views import PostListView, PostDetailView, PostPostedView, PostCategoryView


urlpatterns = [
    path('', PostListView.as_view()),
    path('detail/<str:slug>', PostDetailView.as_view()),
    path('posted/', PostPostedView.as_view()),
    path('category/', PostCategoryView.as_view()),
]