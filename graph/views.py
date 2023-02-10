from django.shortcuts import render
from rest_framework import viewsets
from django.views.generic import TemplateView, ListView

from . import serializers
from . import models

class GraphViewSet(viewsets.ModelViewSet):
    queryset = models.Graph.objects.all()
    serializer_class = serializers.GraphSerializer


class GraphPointViewSet(viewsets.ModelViewSet):
    queryset = models.GraphPoint.objects.all()
    serializer_class = serializers.GraphPointSerializer


class GraphListView(ListView):
    queryset = models.Graph.objects.all()


class IndexView(TemplateView):
    template_name = "index.html"
