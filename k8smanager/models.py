from django.db import models
from urllib3.exceptions import MaxRetryError
from . import k8s


class Cluster(models.Model):
    name = models.CharField(max_length=255)
    cluster_endpoint = models.URLField()

    def __str__(self):
        return self.name

    def get_namespaces(self):
        try:
            client = k8s.get_client(self.cluster_endpoint)
            return k8s.get_namespaces(client)
        except MaxRetryError as e:
            return f"Error: {e}"

    def get_pods_for_namespace(self, namespace):
        try:
            client = k8s.get_client(self.cluster_endpoint)
            return k8s.get_pods_for_namespace(client, namespace)
        except MaxRetryError as e:
            return f"Error: {e}"

    def get_nodes(self):
        try:
            client = k8s.get_client(self.cluster_endpoint)
            return k8s.get_nodes(client)
        except MaxRetryError as e:
            return f"Error: {e}"

    def get_cluster_version(self):
        try:
            client = k8s.get_client(self.cluster_endpoint)
            return k8s.get_cluster_version(client)
        except MaxRetryError as e:
            return f"Error: {e}"


class Node(models.Model):
    name = models.CharField(max_length=255)
    cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Pod(models.Model):
    name = models.CharField(max_length=255)
    cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE)
    namespace = models.CharField(max_length=255)
    status = models.CharField(max_length=255)

    def __str__(self):
        return self.name
