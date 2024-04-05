from django.db import models
import kubernetes
from urllib3.exceptions import MaxRetryError


class Cluster(models.Model):
    name = models.CharField(max_length=255)
    cluster_endpoint = models.URLField()

    def get_namespaces(self):
        try:
            kubernetes.config.load_kube_config()
            client = kubernetes.client.CoreV1Api()
            namespaces = client.list_namespace()
            namespace_list = [namespace.metadata.name for namespace in namespaces.items]
            return namespace_list
        except MaxRetryError as e:
            return f"Error: {e}"

    def __str__(self):
        return self.name
