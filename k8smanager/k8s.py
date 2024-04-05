import kubernetes


def get_client(endpoint: str):
    kubernetes.config.load_kube_config()
    return kubernetes.client.CoreV1Api()


def get_namespaces(client):
    namespaces = client.list_namespace()
    namespace_list = [namespace.metadata.name for namespace in namespaces.items]
    return namespace_list


def get_pods_for_namespace(client, namespace):
    pods = client.list_namespaced_pod(namespace)
    pod_list = [pod.metadata.name for pod in pods.items]
    return pod_list


def get_nodes(client):
    nodes = client.list_node()
    node_list = [node.metadata.name for node in nodes.items]
    return node_list