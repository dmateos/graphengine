from django.db import models
import kubernetes


class Cluster(models.Model):
    name = models.CharField(max_length=255)
    cluster_endpoint = models.URLField()

    def poll_cluster(self):
        config = kubernetes.client.Configuration()
        config.host = self.cluster_endpoint

        client = kubernetes.client.CoreV1Api(
            kubernetes.client.ApiClient(config)
        )

        return client.list_pod_for_all_namespaces()
