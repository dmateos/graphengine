from django.db import models
import transformers


class InferenceModel(models.Model):
    name = models.CharField(max_length=32, null=False)
    model_name = models.CharField(max_length=32, null=False)

    input = models.TextField(null=True, blank=True)
    metadata = models.TextField(null=True, blank=True)
    output = models.TextField(null=True, blank=True)

    def run_model(self):
        model = transformers.pipeline(model=self.model_name)

        if self.model_name == "facebook/bart-large-mnli":
            output = model(self.input, candidate_labels=self.metadata.split(","))
        elif self.model_name == "google/vit-base-patch16-224":
            output = model(images=self.input)
            output = [{"score": round(pred["score"], 4), "label": pred["label"]} for pred in output]
        else:
            raise NotImplementedError()

        self.output = output
        self.save()
