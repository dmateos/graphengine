from django.urls import path
from . import views

urlpatterns = [
    path("aimodel/", views.InferenceListView.as_view(), name="imodel"),
    path("imodels/<int:pk>",
         views.InferenceView.as_view(),
         name="imodel_detail"
         ),
    path("", views.IndexView.as_view()),
]
