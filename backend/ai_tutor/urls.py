from django.urls import path

from .views import AITutorAPI


urlpatterns = [
    path("ai-tutor", AITutorAPI.as_view(), name="ai_tutor_api"),
]
