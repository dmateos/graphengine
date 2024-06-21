import django.test
from .models import InferenceModel
from .views import InferenceView
from rest_framework.test import APIClient


class TestInterenceAPI(django.test.TestCase):
    def test_api_get(self):
        model = InferenceModel.objects.create(
            name="test",
            model_name="test",
            metadata="test-meta",
            output="test-output",
        )

        api_client = APIClient()
        response = api_client.get(f"/calculus/api/models/{model.pk}/")
        self.assertEqual(response.status_code, 200)
        response_parsed = response.json()
        assert response_parsed["output"] == "test-output"


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

    def test_model_get_output(self):
        model = InferenceModel.objects.create(
            name="test",
            model_name="test",
            metadata="test-meta",
            output="test-output",
        )

        output = model.get_output()
        self.assertEqual(output, "test-output")

    def test_model_background_run(self):
        model = InferenceModel.objects.create(
            name="test",
            model_name="test",
            metadata="test-meta",
            output="",
            background=True,
        )

        model.run_model("test-input")
        self.assertEqual(model.output, "")


class TestInferenceView(django.test.TestCase):
    def test_get(self):
        model = InferenceModel.objects.create(
            name="test",
            model_name="test",
            metadata="test-meta",
            output="",
        )

        response = self.client.get(f"/calculus/models/{model.pk}")
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        model = InferenceModel.objects.create(
            name="test",
            model_name="test",
            metadata="test-meta",
            output="",
        )

        response = self.client.post(
            f"/calculus/models/{model.pk}",
            {
                "input": "test-input",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/calculus/models/{model.pk}")
        model.refresh_from_db()
        self.assertEqual(model.output, "test-input test-meta")

    def test_post_image(self):
        model = InferenceModel.objects.create(
            name="test",
            model_name="testImage",
            metadata="test-meta",
            output="image",
            input_type="image",
        )

        with open("calculus/test.jpg", "rb") as f:
            response = self.client.post(
                f"/calculus/models/{model.pk}",
                {
                    "input": f,
                },
            )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/calculus/models/{model.pk}")

    def test_post_invalid(self):
        model = InferenceModel.objects.create(
            name="test",
            model_name="test",
            metadata="test-meta",
            output="",
        )

        response = self.client.post(
            f"/calculus/models/{model.pk}",
            {
                "input": "",
            },
        )

        self.assertEqual(response.status_code, 500)

    def test_get_input_form_returns_text_form(self):
        model = InferenceModel.objects.create(
            name="test",
            model_name="test",
            metadata="test-meta",
            output="",
            input_type="text",
        )

        view = InferenceView()
        input_form = view.get_input_form(model)
        self.assertEqual(input_form.__class__.__name__, "TextInputForm")

    def test_get_input_form_returns_image_form(self):
        model = InferenceModel.objects.create(
            name="test",
            model_name="test",
            metadata="test-meta",
            output="",
            input_type="image",
        )

        view = InferenceView()
        input_form = view.get_input_form(model)
        self.assertEqual(input_form.__class__.__name__, "ImageInputForm")
