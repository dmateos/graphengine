import os
from celery import Celery
from graph import settings


def bootstrap_django():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "l4mbda.settings")
    import django

    django.setup()


def build_app():
    redis = "redis://:{0}@{1}".format(
        settings.REDIS["default"]["PASSWORD"],
        settings.REDIS["default"]["HOST"],
    )
    return Celery("tasks", backend=redis, broker=redis)


bootstrap_django()
app = build_app()


@app.task(bind=True)
def run_job(self, job_id):
    from jobmanager.models import Job

    job_model = Job.objects.get(pk=job_id)
    job_model.run_main()
