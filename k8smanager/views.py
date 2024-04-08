from django.views.generic import TemplateView, ListView
from django.views import View
from .models import Cluster, Pod, Node, Ingress, Deployment, Service
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse


class IndexView(TemplateView):
    template_name = "k8smanager/index.html"


class ClusterListView(ListView):
    model = Cluster
    template_name = "k8smanager/cluster_list.html"


class ClusterDetailView(View):
    def get(self, request, *args, **kwargs):
        cluster = Cluster.objects.get(pk=kwargs["pk"])
        nodes = Node.objects.filter(cluster=cluster)
        ingress = Ingress.objects.filter(cluster=cluster)
        namespace = {}

        for pod in Pod.objects.filter(cluster=cluster):
            if pod.namespace not in namespace:
                namespace[pod.namespace] = {}
            if "pods" not in namespace[pod.namespace]:
                namespace[pod.namespace]["pods"] = []
            namespace[pod.namespace]["pods"].append(pod)

        for deployment in Deployment.objects.filter(cluster=cluster):
            if deployment.namespace not in namespace:
                namespace[deployment.namespace] = {}
            if "deployments" not in namespace[deployment.namespace]:
                namespace[deployment.namespace]["deployments"] = []
            namespace[deployment.namespace]["deployments"].append(deployment)

        for service in Service.objects.filter(cluster=cluster):
            if service.namespace not in namespace:
                namespace[service.namespace] = {}
            if "services" not in namespace[service.namespace]:
                namespace[service.namespace]["services"] = []
            namespace[service.namespace]["services"].append(service)

        return render(
            request,
            "k8smanager/cluster_detail.html",
            {
                "cluster": cluster,
                "namespaces": namespace,
                "nodes": nodes,
                "ingresses": ingress,
            },
        )


class ClusterSyncView(View):
    def get(self, request, *args, **kwargs):
        cluster = Cluster.objects.get(pk=kwargs["pk"])
        cluster.sync()
        return HttpResponseRedirect(
            reverse("cluster_detail", args=[cluster.pk])
        )


class PodDetailView(View):
    def get(self, request, *args, **kwargs):
        cluster = Cluster.objects.get(pk=kwargs["cluster_pk"])
        pod = Pod.objects.get(pk=kwargs["pk"])
        logs = pod.get_logs()

        return render(
            request,
            "k8smanager/pod_detail.html",
            {
                "cluster": cluster,
                "pod": pod,
                "logs": logs,
            },
        )
