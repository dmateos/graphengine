from rest_framework import serializers
from . import models


class GraphSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Graph
        fields = ["points", "name"]


class GraphPointSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.GraphPoint
        fields = ["data"]
