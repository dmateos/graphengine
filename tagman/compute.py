import boto3
import azure.mgmt.compute


def get_aws_vms_with_tag(auth_model, key, value):
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
                if tag["Key"] == key and tag["Value"] == value:
                    vms.append(instance)
    return vms


def get_azure_vm_with_tag(auth_model, key, value):
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
            if tag["Key"] == key and tag["Value"] == value:
                tagged_vms.append(vm)

    return tagged_vms
