from django.db import models


class GraphPoint(models.Model):
    data = models.CharField(max_length=32)


class Graph(models.Model):
    points = models.ForeignKey(GraphPoint, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
