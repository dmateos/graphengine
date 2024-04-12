from django.db import models
import boto3


class Schedule(models.Model):
    name = models.CharField(max_length=255)
    schedule = models.CharField(max_length=255)
    action = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class UniversalTag(models.Model):
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.key}: {self.value}"

    def get_aws_vms_with_tag(self):
        aws = boto3.client("ec2")
        instances = aws.describe_instances()
        vms = []
        for reservation in instances["Reservations"]:
            for instance in reservation["Instances"]:
                for tag in instance["Tags"]:
                    if tag["Key"] == self.key and tag["Value"] == self.value:
                        vms.append(instance)

    def get_azure_vms_with_tag(self):
        pass
