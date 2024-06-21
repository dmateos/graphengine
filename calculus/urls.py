from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r"models", views.InferenceViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("models/", views.InferenceListView.as_view(), name="model"),
    path("models/<int:pk>", views.InferenceView.as_view(), name="model_detail"),
    path("", views.IndexView.as_view()),
]
