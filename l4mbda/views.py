from django.http.response import HttpResponseRedirect
from django.views.generic import ListView, TemplateView
from .models import Job, JobRun


def run_job(request, job_id):
    job = Job.objects.get(pk=job_id)
    job.run()
    return HttpResponseRedirect("/l4mbda/jobs")


class IndexView(TemplateView):
    template_name = "l4mbda/index.html"


class JobView(ListView):
    model = Job

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class JobRunView(ListView):
    model = JobRun
