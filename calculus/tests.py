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


class TestInferenceView(django.test.TestCase):
    def test_get(self):
        model = InferenceModel.objects.create(
            name="test",
            model_name="test",
            metadata="test-meta",
            output="",
        )

        response = self.client.get(f"/calculus/imodels/{model.pk}")
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        model = InferenceModel.objects.create(
            name="test",
            model_name="test",
            metadata="test-meta",
            output="",
        )

        response = self.client.post(f"/calculus/imodels/{model.pk}", {
            "input": "test-input",
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/calculus/imodels/{model.pk}")
        model.refresh_from_db()
        self.assertEqual(model.output, "test-input test-meta")
