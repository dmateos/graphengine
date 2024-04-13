from django.db import models
from . import compute


class Schedule(models.Model):
    name = models.CharField(max_length=255)
    schedule = models.CharField(max_length=255)
    action = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class AWSAccessDetails(models.Model):
    access_key = models.CharField(max_length=255)
    secret_key = models.CharField(max_length=255)
    region = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.access_key} - {self.region}"


class AzureAccessDetails(models.Model):
    subscription_id = models.CharField(max_length=255)
    client_id = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)
    tenant = models.CharField(max_length=255)

    def __str__(self):
        return self.subscription_id


class EventLog(models.Model):
    event = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True)
    machine_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.event} - {self.time}"


class UniversalTag(models.Model):
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    schedules = models.ManyToManyField(Schedule)

    def __str__(self):
        return f"{self.key}: {self.value}"

    def get_aws_vms_with_tag(self, auth_model):
        return compute.get_aws_vms_with_tag(
            auth_model,
            self.key,
            self.value
        )

    def get_azure_vms_with_tag(self, auth_model):
        return compute.get_azure_vm_with_tag(
            auth_model,
            self.key,
            self.value
        )
