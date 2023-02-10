from django.db import models

GRAPHTYPE_LINE = "line"
GRAPHTYPE_BAR = "bar"


class GraphPoint(models.Model):
    data = models.CharField(max_length=32)


class Graph(models.Model):
    points = models.ForeignKey(GraphPoint, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    type = models.CharField(max_length=16, default=GRAPHTYPE_LINE, choices=(
        (GRAPHTYPE_LINE, "line"),
        (GRAPHTYPE_BAR, "bar"),
    ))
