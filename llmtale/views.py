from django.views.generic import TemplateView, ListView
from django.views import View
from django.shortcuts import render
from . import models
from . import forms


class IndexView(TemplateView):
    template_name = "llmtale/index.html"


class LLMAgentListView(ListView):
    model = models.Agent
    template_name = "llmtale/llmagent_list.html"


class LLMAgentView(View):
    def get(self, request, pk):
        model = models.Agent.objects.get(pk=pk)
        form = forms.TextInputForm()
        return render(
            request,
            "llmtale/llmagent_detail.html",
            {"model": model, "form": form}
        )

    def post(self, request, pk):
        pass
