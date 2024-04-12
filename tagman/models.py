from django.db import models
import boto3
import azure.mgmt.compute


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


class UniversalTag(models.Model):
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    schedules = models.ManyToManyField(Schedule)

    def __str__(self):
        return f"{self.key}: {self.value}"

    def get_aws_vms_with_tag(self, auth_model):
        aws = boto3.client(
            "ec2",
            region_name=auth_model.region,
            aws_access_key_id=auth_model.access_key,
            aws_secret_access_key=auth_model.secret_key,
        )
        instances = aws.describe_instances()
        vms = []
        for reservation in instances["Reservations"]:
            for instance in reservation["Instances"]:
                for tag in instance["Tags"]:
                    if tag["Key"] == self.key and tag["Value"] == self.value:
                        vms.append(instance)

        return vms

    def get_azure_vms_with_tag(self, auth_model):
        azure_con = azure.mgmt.compute.ComputeManagementClient(
            azure.common.credentials.ServicePrincipalCredentials(
                client_id=auth_model.client_id,
                secret=auth_model.secret,
                tenant=auth_model.tenant,
            ),
            auth_model.subscription_id,
        )

        vms = azure_con.virtual_machines.list_all()
        tagged_vms = []
        for vm in vms:
            for tag in vm.tags:
                if tag["Key"] == self.key and tag["Value"] == self.value:
                    tagged_vms.append(vm)

        return tagged_vms
