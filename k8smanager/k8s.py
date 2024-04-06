import kubernetes


def get_client(endpoint: str):
    kubernetes.config.load_kube_config()
    return kubernetes.client.CoreV1Api()


# Does not work
def get_cluster_version(client):
    api_instance = kubernetes.client.VersionApi(client)
    response = api_instance.get_code()
    return response


def get_namespaces(client):
    namespaces = client.list_namespace()
    namespace_list = [namespace.metadata.name for namespace in namespaces.items]
    return namespace_list


def get_pods_for_namespace(client, namespace):
    pods = client.list_namespaced_pod(namespace)
    pod_list = []
    for pod in pods.items:
        pod_list.append({
            "name": pod.metadata.name,
            "ip": pod.status.pod_ip,
            "start_time": pod.status.start_time,
            "status": pod.status.phase,
            "node": pod.spec.node_name,
        })
    return pod_list


def get_nodes(client):
    nodes = client.list_node()
    node_list = [node.metadata.name for node in nodes.items]
    return node_list


def get_ingresses(client):
    api_instance = kubernetes.client.NetworkingV1Api()
    ingresses = api_instance.list_ingress_for_all_namespaces()

    ingress_list = []
    for ingress in ingresses.items:
        ingress_list.append({
            "name": ingress.metadata.name,
            "namespace": ingress.metadata.namespace,
            "rules": ingress.spec.rules[0],
        })
    return ingress_list
