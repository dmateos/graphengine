from django.db import models
from . import drivers
import base64

SUPPORTED_OUTPUT_TYPES = [
    "text",
    "text_stream",
    "image",
    "image_stream"
]

SUPPORTED_INPUT_TYPES = [
    "text",
    "image",
]


class InferenceModel(models.Model):
    name = models.CharField(max_length=32, null=False)
    model_name = models.CharField(
        max_length=32,
        null=False,
        choices=[(k, k) for k in drivers.SUPPORTED_MODELS.keys()]
    )

    metadata = models.TextField(null=True, blank=True)
    output = models.TextField(null=True, blank=True)

    output_type = models.CharField(
        max_length=32,
        default="text",
        choices=[(k, k) for k in SUPPORTED_OUTPUT_TYPES]
    )

    input_type = models.CharField(
        max_length=32,
        default="text",
        choices=[(k, k) for k in SUPPORTED_INPUT_TYPES]
    )

    def __str__(self):
        return f"{self.name} {self.model_name}"

    def run_model(self, input=None):
        try:
            driver = drivers.SUPPORTED_MODELS[self.model_name]
        except KeyError:
            raise NotImplementedError()

        self.output = driver.run(input, self.metadata)
        self.save()

    def get_output(self):
        if self.output_type == "text":
            return self.output
        elif self.output_type == "image":
            return base64.b64decode(self.output)
        else:
            raise NotImplementedError()

    def set_output(self, output):
        if self.output_type == "text":
            self.output = output
        elif self.output_type == "image":
            self.output = base64.b64encode(output)
        else:
            raise NotImplementedError()
