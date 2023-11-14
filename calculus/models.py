from django.db import models
from . import drivers


class InferenceModel(models.Model):
    name = models.CharField(max_length=32, null=False)
    model_name = models.CharField(
        max_length=32,
        null=False,
        choices=[(k, k) for k in drivers.SUPPORTED_MODELS.keys()]
    )

    input = models.TextField(null=True, blank=True)
    metadata = models.TextField(null=True, blank=True)
    output = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.model_name}"

    def run_model(self):
        try:
            driver = drivers.SUPPORTED_MODELS[self.model_name]
        except KeyError:
            raise NotImplementedError()

        self.output = driver.run(self.input, self.metadata)
        self.save()
