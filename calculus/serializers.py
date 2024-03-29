from rest_framework import serializers
from . import models


class InferenceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InferenceModel
        fields = [
            "name",
            "model_name",
            "metadata",
            "output",
            "output_type",
            "input_type",
        ]
