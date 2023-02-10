from django.db import models

GRAPHTYPE_LINE = "line"
GRAPHTYPE_BAR = "bar"


class Graph(models.Model):
    name = models.CharField(max_length=32)
    type = models.CharField(max_length=16, default=GRAPHTYPE_LINE, choices=(
        (GRAPHTYPE_LINE, "line"),
        (GRAPHTYPE_BAR, "bar"),
    ))

    def get_points(self):
        return [1, 2, 3, 4, 5]*4

    def get_labels(self):
        return [1, 2, 3, 4, 5]*4


class GraphPoint(models.Model):
    data = models.CharField(max_length=32)
    graph = models.ForeignKey(Graph, on_delete=models.CASCADE, null=False)
