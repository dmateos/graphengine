from django.db import models


ETL_STATUS = (
    ("RUNNING", "RUNNING"),
    ("SUCCESS", "SUCCESS"),
    ("FAILED", "FAILED"),
    ("ERROR", "ERROR"),

)

ETL_INPUT_TYPE = (

)

ETL_INPUT_FORMAT = (

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


class ETLInput(models.Model):
    connection_string = models.TextField()
    connection_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ETLOutput(models.Model):
    job = models.ForeignKey(ETLJob, on_delete=models.CASCADE)
    data = models.TextField()

    def __str__(self):
        return self.name
