import django.test
from unittest.mock import patch
from .models import InferenceModel


class TestInterenceModelRun(django.test.TestCase):
    def test_model_run(self):
        model = InferenceModel.objects.create(
            name="test",
            model_name="test",
            input="test",
            metadata="test",
            output="",
        )

        model.run_model()
        self.assertEqual(model.output, "test")
