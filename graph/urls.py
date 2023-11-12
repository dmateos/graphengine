from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r"graphs", views.GraphViewSet)
router.register(r"graphpoints", views.GraphPointViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("", views.GraphListView.as_view()),
    path("<int:pk>", views.GraphDetailView.as_view(), name="graphs"),
    path("", views.IndexView.as_view()),
]
