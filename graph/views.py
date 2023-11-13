from django.views.generic import TemplateView, ListView, DetailView
from django_filters import rest_framework as filters
from rest_framework import viewsets
from . import serializers
from . import models


class GraphPointFilter(filters.FilterSet):
    sequence = filters.NumberFilter(field_name="sequence", lookup_expr="gt")

    class Meta:
        model = models.GraphPoint
        fields = ("graph",)


class IndexView(TemplateView):
    template_name = "index.html"


class GraphViewSet(viewsets.ModelViewSet):
    queryset = models.Graph.objects.all()
    serializer_class = serializers.GraphSerializer


class GraphPointViewSet(viewsets.ModelViewSet):
    queryset = models.GraphPoint.objects.all()
    serializer_class = serializers.GraphPointSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = GraphPointFilter


class GraphListView(ListView):
    queryset = models.Graph.objects.all()


class GraphDetailView(DetailView):
    model = models.Graph
