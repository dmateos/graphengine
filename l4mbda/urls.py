from django.urls import path
from . import views

urlpatterns = [
    path("", views.root),
    path("jobs", views.JobView.as_view()),
    path("jobruns", views.JobRunView.as_view()),
    path("runjob/<int:job_id>", views.run_job),
]
