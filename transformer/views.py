from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView
from django.views import View
from django.urls import reverse
from .models import ETLJob


class IndexView(TemplateView):
    template_name = "transformer/index.html"


class JobView(ListView):
    model = ETLJob


class JobRunView(View):
    def get(self, request, pk):
        job = ETLJob.objects.get(pk=pk)
        job.run_etl()
        return HttpResponseRedirect(reverse("jobs"))
