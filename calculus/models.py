from django.db import models
from . import drivers

SUPPORTED_MODELS = {
    "facebook/bart-large-mnli": {
        "driver": drivers.BartLaegeMNLI()
    },
    "google/vit-base-patch16-224": {
        "driver": drivers.VitBasePatch16_224()
    },
}


class InferenceModel(models.Model):
    name = models.CharField(max_length=32, null=False)
    model_name = models.CharField(
        max_length=32,
        null=False,
        choices=[(k, k) for k in SUPPORTED_MODELS.keys()]
    )

    input = models.TextField(null=True, blank=True)
    metadata = models.TextField(null=True, blank=True)
    output = models.TextField(null=True, blank=True)

    def run_model(self):
        try:
            driver = SUPPORTED_MODELS[self.model_name]["driver"]
        except KeyError:
            raise NotImplementedError()

        self.output = driver.run(self.input, self.metadata)
        self.save()
