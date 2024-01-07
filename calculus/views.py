from django.views.generic import TemplateView, ListView
from django.views import View
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from rest_framework import viewsets
from . import models
from . import serializers
from . import forms


class IndexView(TemplateView):
    template_name = "calculus/index.html"


class InferenceListView(ListView):
    template_name = "calculus/inference_list.html"
    queryset = models.InferenceModel.objects.all()


class InferenceView(View):
    def get_input_form(self, model, post_data=None, file_data=None):
        if model.input_type == "text":
            return forms.TextInputForm(post_data)
        elif model.input_type == "image":
            return forms.ImageInputForm(post_data, file_data)

    def get(self, request, pk):
        model = models.InferenceModel.objects.get(pk=pk)
        input_form = self.get_input_form(model)

        return render(
            request,
            "calculus/inference_detail.html",
            {"model": model, "form": input_form}
        )

    def post(self, request, pk):
        model = models.InferenceModel.objects.get(pk=pk)
        input_form = self.get_input_form(model, request.POST, request.FILES)

        if input_form.is_valid():
            model_input = input_form.cleaned_data["input"]
            model.run_model(model_input)
        else:
            return HttpResponse(status=500)

        return HttpResponseRedirect(reverse("model_detail", args=[pk]))


class InferenceViewSet(viewsets.ModelViewSet):
    queryset = models.InferenceModel.objects.all()
    serializer_class = serializers.InferenceModelSerializer
