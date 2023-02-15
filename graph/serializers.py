from rest_framework import serializers
from . import models


class GraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Graph
        fields = ["name", "type"]


class GraphPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GraphPoint
        fields = ["label", "data", "graph", "created", "sequence"]
