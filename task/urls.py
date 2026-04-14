from django.urls import path
from .views import BlogConversionView

urlpatterns = (
    path("ai-storytelling/", BlogConversionView.as_view(), name="ai_writing"),
    # Path for the GET (Polling the specific task status)
    path("ai-storytelling/<uuid:task_id>/", BlogConversionView.as_view(), name="conversion_status"),
)