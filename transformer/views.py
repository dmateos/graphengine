from django.views.generic import TemplateView, ListView
from .models import ETLJob


class IndexView(TemplateView):
    template_name = "transformer/index.html"


class JobView(ListView):
    model = ETLJob
