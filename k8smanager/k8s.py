import kubernetes
import pydantic


class ServiceModel(pydantic.BaseModel):
    name: str
    namespace: str
    cluster_ip: str
    external_ip: str | None
    type: str
    ports: list


class DeploymentModel(pydantic.BaseModel):
    name: str
    namespace: str
    replicas: int
    available_replicas: int | None


class PodModel(pydantic.BaseModel):
    name: str
    ip: str
    start_time: str
    status: str
    node: str


class IngressModel(pydantic.BaseModel):
    name: str
    namespace: str
    rules: str
    ip: str


def get_client(endpoint: str):
    kubernetes.config.load_kube_config()
    return kubernetes.client.CoreV1Api()


# Does not work
def get_cluster_version(client):
    api_instance = kubernetes.client.VersionApi(client)
    response = api_instance.get_code()
    return response


def get_namespaces(client):
    ns = client.list_namespace()
    ns_list = [n.metadata.name for n in ns.items]
    return ns_list


def get_nodes(client):
    nodes = client.list_node()
    node_list = [node.metadata.name for node in nodes.items]
    return node_list


def get_services_for_namespace(client, namespace):
    services = client.list_namespaced_service(namespace)
    service_list = []

    for service in services.items:
        service_model = ServiceModel(
            name=service.metadata.name,
            namespace=service.metadata.namespace,
            cluster_ip=service.spec.cluster_ip,
            external_ip=service.spec.external_i_ps,
            type=service.spec.type,
            ports=service.spec.ports,
        )
        service_list.append(service_model)
    return service_list


def get_deployments_for_namespace(client, namespace):
    deployments_api = kubernetes.client.AppsV1Api()
    deployments = deployments_api.list_namespaced_deployment(namespace)
    deployment_list = []

    for deployment in deployments.items:
        deployment_model = DeploymentModel(
            name=deployment.metadata.name,
            namespace=deployment.metadata.namespace,
            replicas=deployment.spec.replicas,
            available_replicas=deployment.status.available_replicas,
        )
        deployment_list.append(deployment_model)
    return deployment_list


def get_pods_for_namespace(client, namespace):
    pods = client.list_namespaced_pod(namespace)
    pod_list = []

    for pod in pods.items:
        pod_model = PodModel(
            name=pod.metadata.name,
            ip=pod.status.pod_ip,
            start_time=str(pod.status.start_time),
            status=pod.status.phase,
            node=pod.spec.node_name,
        )
        pod_list.append(pod_model)
    return pod_list


def get_ingresses(client):
    api_instance = kubernetes.client.NetworkingV1Api()
    ingresses = api_instance.list_ingress_for_all_namespaces()
    ingress_list = []

    for ingress in ingresses.items:
        ingress_model = IngressModel(
            name=ingress.metadata.name,
            namespace=ingress.metadata.namespace,
            rules=str(ingress.spec.rules[0]),
            ip=ingress.status.load_balancer.ingress[0].ip,
        )
        ingress_list.append(ingress_model)
    return ingress_list


def get_logs_for_pod(client, namespace, pod_name):
    logs = client.read_namespaced_pod_log(pod_name, namespace)
    return logs
