from django.db import models


class Job(models.Model):
    name = models.CharField(max_length=32, default="new job")
    code = models.TextField()
    times_to_run = models.IntegerField(default=1)

    # TODO should be in job run, race condition?
    storage = models.TextField(default="", null=True, blank=True)

    next_job = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.name} {self.id}"

    def run(self):
        from l4mbda.tasks import run_job

        for _ in range(0, self.times_to_run):
            run_job.delay(self.id)
        return True

    def run_main(self):
        state = JobRun.objects.create(job=self)
        injected_globals = {}  # can restrict
        injected_locals = {"storage": self.storage}

        try:
            state.set_state("running")
            exec(self.code, injected_globals, injected_locals)
            self.storage = injected_locals["storage"]
            self.save()

            if self.next_job:
                self.next_job.storage = self.storage
                self.next_job.save()
                self.next_job.run_main()

            state.set_status("ok")
        except Exception as e:
            state.set_status("error")
            state.set_job_message(str(e))
        finally:
            state.set_state("done")


class JobRun(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    job_message = models.TextField(default="")

    state = models.CharField(
        max_length=16,
        default="not-run",
        choices=(("not-run", "not-run"), ("running", "running"), ("done", "done")),
    )

    status = models.CharField(
        max_length=16,
        default="none",
        choices=(("none", "none"), ("ok", "ok"), ("error", "error")),
    )

    def __str__(self):
        return f"{self.job.id} {self.state} {self.status}"

    def set_state(self, state):
        self.state = state
        self.save()

    def set_status(self, status):
        self.status = status
        self.save()

    def set_job_message(self, message):
        self.job_message = message
        self.save()


class JobInput(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.job.id}"
