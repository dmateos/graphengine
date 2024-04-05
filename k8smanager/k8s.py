import kubernetes


def get_client(endpoint: str):
    kubernetes.config.load_kube_config()
    return kubernetes.client.CoreV1Api()


def get_namespaces(client):
    namespaces = client.list_namespace()
    namespace_list = [namespace.metadata.name for namespace in namespaces.items]
    return namespace_list
