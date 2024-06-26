from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("jobs/", views.JobView.as_view(), name="jobs"),
    path("runjob/<int:pk>", views.JobRunView.as_view(), name="runjob"),
]
