from django.urls import path
from . import views

urlpatterns = [
    path("aimodel/", views.InferenceListView.as_view()),
    path("runmodel/<int:model_id>", views.run_model),
    path("", views.IndexView.as_view()),
]
