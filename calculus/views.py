from django.views.generic import TemplateView, ListView
from django.views import View
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import models
from . import forms


class IndexView(TemplateView):
    template_name = "calculus/index.html"


class InferenceListView(ListView):
    template_name = "calculus/inference_list.html"
    queryset = models.InferenceModel.objects.all()


class InferenceView(View):
    def get(self, request, pk):
        model = models.InferenceModel.objects.get(pk=pk)
        input_form = forms.InputForm()

        return render(
            request,
            "calculus/inference_detail.html",
            {"model": model, "form": input_form}
        )

    def post(self, request, pk):
        model = models.InferenceModel.objects.get(pk=pk)
        input_form = forms.InputForm(request.POST)

        if input_form.is_valid():
            model_input = input_form.cleaned_data["input"]
            model.run_model(model_input)

        return HttpResponseRedirect(reverse("imodel_detail", args=[pk]))
