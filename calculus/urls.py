from django.urls import path
from . import views

urlpatterns = [
    path("models/", views.InferenceListView.as_view(), name="model"),
    path("models/<int:pk>",
         views.InferenceView.as_view(),
         name="model_detail"
         ),
    path("", views.IndexView.as_view()),
]
