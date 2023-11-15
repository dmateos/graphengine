from django.http.response import HttpResponseRedirect
from django.views.generic import ListView, TemplateView
from django.views import View
from django.urls import reverse
from .models import Job, JobRun


class IndexView(TemplateView):
    template_name = "l4mbda/index.html"


class JobView(ListView):
    model = Job

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class JobRunView(ListView):
    model = JobRun


class JobRunnerView(View):
    def get(self, request, pk):
        job = Job.objects.get(pk=pk)
        job.run()
        return HttpResponseRedirect(reverse("job_list"))
