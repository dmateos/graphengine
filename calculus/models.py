from django.db import models
import transformers

# Create your models here.


class InferenceModel(models.Model):
    name = models.CharField(max_length=32, null=False)
    model_name = models.CharField(max_length=32, null=False)

    def load_model(self):
        model = transformers.Pipeline(model=self.model_name)
        model("test", candidate_labels=["test"])