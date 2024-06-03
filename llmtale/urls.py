from django.urls import path
from . import views


urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("agents", views.LLMAgentListView.as_view(), name="agents"),
    path("agents/<int:pk>", views.LLMAgentView.as_view(), name="agent_detail"),
]
