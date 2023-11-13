from django.views.generic import TemplateView, ListView
from . import models
from django.http.response import HttpResponseRedirect


def run_model(request, model_id):
    model = models.InferenceModel.objects.get(pk=model_id)
    model.run_model()
    return HttpResponseRedirect("/calculus/aimodel")


class IndexView(TemplateView):
    template_name = "calculus/index.html"


class InferenceListView(ListView):
    template_name = "calculus/inference_list.html"
    queryset = models.InferenceModel.objects.all()
