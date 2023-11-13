from django.db import models
import transformers

# Create your models here.


class InferenceModel(models.Model):
    name = models.CharField(max_length=32, null=False)
    model_name = models.CharField(max_length=32, null=False)

    input = models.TextField(null=True, blank=True)
    metadata = models.TextField(null=True, blank=True)
    output = models.TextField(null=True, blank=True)

    def run_model(self):
        model = transformers.pipeline(model=self.model_name)
        output = model(self.input, candidate_labels=self.metadata.split(","))

        self.output = output
        self.save()
