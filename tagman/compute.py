import boto3
import azure.mgmt.compute
import pydantic


class VmModel(pydantic.BaseModel):
    id: str
    state: str
    type: str


def aws_auth(auth_model):
    return boto3.client(
        "ec2",
        region_name=auth_model.region,
        aws_access_key_id=auth_model.access_key,
        aws_secret_access_key=auth_model.secret_key,
    )


def azure_auth(auth_model):
    return azure.mgmt.compute.ComputeManagementClient(
        azure.common.credentials.ServicePrincipalCredentials(
            client_id=auth_model.client_id,
            secret=auth_model.secret,
            tenant=auth_model.tenant,
        ),
        auth_model.subscription_id,
    )


def get_aws_vms_with_tag(auth_model, key, value):
    aws = aws_auth(auth_model)
    instances = aws.describe_instances()
    vms = []

    for reservation in instances["Reservations"]:
        for instance in reservation["Instances"]:
            for tag in instance["Tags"]:
                if tag["Key"] == key and tag["Value"] == value:
                    vm_model = VmModel(
                        id=instance["InstanceId"],
                        state=instance["State"]["Name"],
                        type=instance["InstanceType"],
                    )
                    vms.append(vm_model)
    return vms


def get_azure_vm_with_tag(auth_model, key, value):
    azure_con = azure_auth(auth_model)
    vms = azure_con.virtual_machines.list_all()
    tagged_vms = []
    for vm in vms:
        for tag in vm.tags:
            if tag["Key"] == key and tag["Value"] == value:
                vm_model = VmModel(
                    id=vm.id,
                    state=vm.instance_view.statuses[1].display_status,
                    type=vm.hardware_profile.vm_size,
                )
                tagged_vms.append(vm_model)
    return tagged_vms


def shutdown_or_startup_aws_vm(auth_model, vm_id, action):
    aws = aws_auth(auth_model)

    if action == "shutdown":
        aws.stop_instances(InstanceIds=[vm_id])
    elif action == "startup":
        aws.start_instances(InstanceIds=[vm_id])


def shutdown_or_startup_azure_vm(auth_model, vm_id, action):
    azure_con = azure_auth(auth_model)

    if action == "shutdown":
        azure_con.virtual_machines.power_off(auth_model.resource_group, vm_id)
    elif action == "startup":
        azure_con.virtual_machines.start(auth_model.resource_group, vm_id)
