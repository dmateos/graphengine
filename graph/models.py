from django.db import models

GRAPHTYPE_LINE = "line"
GRAPHTYPE_BAR = "bar"


class Graph(models.Model):
    name = models.CharField(max_length=32, null=False)
    type = models.CharField(max_length=16, null=False, default=GRAPHTYPE_LINE, choices=(
        (GRAPHTYPE_LINE, "line"),
        (GRAPHTYPE_BAR, "bar"),
    ))

    def get_points(self):
        data = [float(n.data) for n in self.graphpoint_set.all()]
        return data

    def get_labels(self):
        label = [float(n.label) for n in self.graphpoint_set.all()]
        return label


class GraphPoint(models.Model):
    data = models.CharField(max_length=32, null=False)
    label = models.CharField(max_length=8, default=0, null=False)
    graph = models.ForeignKey(Graph, on_delete=models.CASCADE, null=False)
