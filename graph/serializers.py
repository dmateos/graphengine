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

    def create(self, validated_data):
        # TODO: handle missing fields
        graph = validated_data.pop("graph")
        label = validated_data.pop("label")
        data = validated_data.pop("data")
        return graph.create_point(label, data)
