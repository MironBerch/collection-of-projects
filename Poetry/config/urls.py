from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response


class IndexPage(APIView):
    def get(self, request):
        return Response(
            {
                'message': 'Hello World!'
            }
        )


class AboutPage(APIView):
    def get(self, request):
        return Response(
            {
                'message': 'Page which told about theme of project.',
                'theme': 'Poetry'
            }
        )


urlpatterns = [
    path('', IndexPage.as_view()),
    path('about/', AboutPage.as_view()),
]
