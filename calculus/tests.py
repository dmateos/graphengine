import django.test
from .models import InferenceModel


class TestInterenceModelRun(django.test.TestCase):
    def test_model_run(self):
        model = InferenceModel.objects.create(
            name="test",
            model_name="test",
            metadata="test-meta",
            output="",
        )

        model.run_model("test-input")
        self.assertEqual(model.output, "test-input test-meta")
