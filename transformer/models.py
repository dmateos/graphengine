from django.db import models


ETL_STATUS = (
    ("RUNNING", "RUNNING"),
    ("SUCCESS", "SUCCESS"),
    ("FAILED", "FAILED"),
    ("ERROR", "ERROR"),

)

ETL_INPUT_TYPE = (
    ("FILE_CSV", "FILE_CSV"),
)


class ETLJob(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=100, choices=ETL_STATUS)
    error_message = models.TextField()

    etl_input = models.ForeignKey("ETLInput", on_delete=models.CASCADE)
    etl_output = models.ForeignKey("ETLOutput", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def run_etl(self):
        from l4mbda.tasks import run_etl
        run_etl.delay(self.id)

    def run(self):
        try:
            self.status = "SUCCESS"
        except Exception as e:
            self.status = "ERROR"
            self.error_message = str(e)
        finally:
            self.save()


class ETLInput(models.Model):
    connection_string = models.TextField()
    connection_type = models.CharField(max_length=100, choices=ETL_INPUT_TYPE)

    def __str__(self):
        return self.name


class ETLOutput(models.Model):
    job = models.ForeignKey(ETLJob, on_delete=models.CASCADE)
    data = models.TextField()

    def __str__(self):
        return self.name
