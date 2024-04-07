from django.db import models
from . import k8s


class Cluster(models.Model):
    name = models.CharField(max_length=255)
    cluster_endpoint = models.URLField()

    def __str__(self):
        return self.name

    def sync(self):
        self.clean_unfound_resources()

        client = k8s.get_client(self.cluster_endpoint)
        nodes = k8s.get_nodes(client)

        for node in nodes:
            node_obj, _ = Node.objects.get_or_create(
                name=node, cluster=self, status="Unknown"
            )
            node_obj.save()

        for namespace in k8s.get_namespaces(client):
            if namespace != "kube-system":
                pods = k8s.get_pods_for_namespace(client, namespace)
                for pod in pods:
                    node_obj = Node.objects.get(name=pod["node"])
                    pod_obj, _ = Pod.objects.get_or_create(
                        name=pod["name"],
                        cluster=self,
                        node=node_obj,
                        namespace=namespace,
                        status=pod["status"],
                        start_time=pod["start_time"],
                        ip_address=pod["ip"],
                    )
                    pod_obj.save()

        ingresses = k8s.get_ingresses(client)
        for ingress in ingresses:
            ingress_obj, _ = Ingress.objects.get_or_create(
                name=ingress["name"],
                cluster=self,
                namespace=ingress["namespace"],
                rules=ingress["rules"],
                ip_address=ingress["ip"],
                host=ingress["rules"].host,
            )
            ingress_obj.save()

    def clean_unfound_resources(self):
        client = k8s.get_client(self.cluster_endpoint)
        nodes = k8s.get_nodes(client)
        for node in Node.objects.filter(cluster=self):
            if node.name not in nodes:
                node.delete()

        for namespace in k8s.get_namespaces(client):
            if namespace != "kube-system":
                pods = k8s.get_pods_for_namespace(client, namespace)
                for pod in Pod.objects.filter(cluster=self, namespace=namespace):
                    found = False
                    for p in pods:
                        if p["name"] == pod.name:
                            found = True
                            break
                    if not found:
                        pod.delete()

        ingresses = k8s.get_ingresses(client)
        for ingress in Ingress.objects.filter(cluster=self):
            found = False
            for i in ingresses:
                if i["name"] == ingress.name:
                    found = True
                    break
            if not found:
                ingress.delete()


class Node(models.Model):
    name = models.CharField(max_length=255)
    cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Ingress(models.Model):
    name = models.CharField(max_length=255)
    cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE)
    namespace = models.CharField(max_length=255)
    rules = models.TextField()
    host = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return self.name


class Pod(models.Model):
    name = models.CharField(max_length=255)
    cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE)
    node = models.ForeignKey(Node, on_delete=models.CASCADE)

    namespace = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return self.name


class Deployment(models.Model):
    name = models.CharField(max_length=255)
    cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE)
    namespace = models.CharField(max_length=255)
    replicas = models.IntegerField()
    available_replicas = models.IntegerField()
    unavailable_replicas = models.IntegerField()
    strategy = models.TextField()
    template = models.TextField()

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=255)
    cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE)
    namespace = models.CharField(max_length=255)
    cluster_ip = models.GenericIPAddressField()
    external_ip = models.GenericIPAddressField()
    type = models.CharField(max_length=255)
    ports = models.TextField()

    def __str__(self):
        return self.name
