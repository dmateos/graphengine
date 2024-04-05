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
