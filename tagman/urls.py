from django.urls import path
from . import views


urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("tags/", views.TagListView.as_view(), name="tags"),
    path("tags/<int:pk>/", views.TagDetailView.as_view(), name="tag_detail"),
]
