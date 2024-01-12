from django.db import models
from . import drivers
import base64

SUPPORTED_OUTPUT_TYPES = [
    "text",
    "image",
    "image_stream",
    # Not implemented
    "text_stream",
    "data_frame",
    "graphengine_graph"
    "image_and_text",
    "l4mbda"
]

SUPPORTED_INPUT_TYPES = [
    "text",
    "image",
]


class InferenceModel(models.Model):
    name = models.CharField(max_length=32, null=False)
    metadata = models.TextField(null=True, blank=True)
    output = models.TextField(null=True, blank=True)
    background = models.BooleanField(default=False)

    model_name = models.CharField(
        max_length=32,
        null=False,
        choices=[(k, k) for k in drivers.SUPPORTED_MODELS.keys()]
    )

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
        if self.background:
            from l4mbda.tasks import run_model
            if self.input_type != "image":
                data = {
                    "model_id": self.id,
                    "input": input
                }
            else:
                # For some reason were limited with what we can serialize and
                # send to a celery job.
                data = {
                    "model_id": self.id,
                    "input": str(base64.b64encode(input.file.read()))
                }
            run_model.delay(data)
        else:
            self.run(input)

    def run(self, input=None):
        try:
            driver = drivers.SUPPORTED_MODELS[self.model_name]
        except KeyError:
            raise NotImplementedError()

        self.output = driver.run(input, self.metadata)
        self.save()

    def get_output(self):
        return self.output


class InferenceCache(models.Model):
    model = models.ForeignKey(InferenceModel, on_delete=models.CASCADE)
    input = models.TextField(null=False, blank=False)
    output = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.model} {self.input}"

    def get_output(self):
        return self.output
