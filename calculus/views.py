from django.views.generic import TemplateView, ListView
from . import models


class IndexView(TemplateView):
    template_name = "calculus/index.html"


class InterenceListView(ListView):
    template_name = "calculus/inference_list.html"
    queryset = models.InferenceModel.objects.all()
