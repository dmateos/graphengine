from django.db import models


class ETLJob(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=100)
    success = models.BooleanField()
    error_message = models.TextField()

    def __str__(self):
        return self.name


class ETLConnection(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    connection_string = models.TextField()
    connection_type = models.CharField(max_length=100)
    connection_status = models.CharField(max_length=100)
    last_successful_connection = models.DateTimeField()
    last_failed_connection = models.DateTimeField()
    last_error_message = models.TextField()

    def __str__(self):
        return self.name