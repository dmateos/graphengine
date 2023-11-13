from django.urls import path
from . import views

urlpatterns = [
    path("aimodel/", views.InterenceListView.as_view()),
    path("", views.IndexView.as_view()),
]
