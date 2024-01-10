import os
from celery import Celery
from graphengine import settings


def bootstrap_django():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graphengine.settings")
    import django

    django.setup()


def build_app():
    if settings.REDIS["default"].get("PASSWORD", None):
        redis = "redis://:@{0}".format(
            settings.REDIS["default"]["HOST"],
        )
    else:
        redis = "redis://:{0}@{1}".format(
            settings.REDIS["default"]["PASSWORD"],
            settings.REDIS["default"]["HOST"],
        )
    return Celery("tasks", backend=redis, broker=redis)


bootstrap_django()
app = build_app()


@app.task(bind=True)
def run_model(self, job_id):
    from calculus.models import InferenceModel

    model = InferenceModel.objects.get(pk=job_id)
