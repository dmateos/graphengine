from django.urls import path
from . import views

urlpatterns = [
    path("jobs/", views.JobView.as_view(), name="job_list"),
    path("jobruns/", views.JobRunView.as_view()),
    path("runjob/<int:pk>", views.JobRunnerView.as_view()),
    path("", views.IndexView.as_view()),
]
