from django.views.generic import TemplateView, ListView
from django.views import View
from .models import Cluster, Pod, Node
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
        ingress = cluster.get_ingresses()

        pods = {}
        for pod in Pod.objects.filter(cluster=cluster):
            if pod.namespace not in pods:
                pods[pod.namespace] = []
            pods[pod.namespace].append(pod)

        return render(
            request,
            "k8smanager/cluster_detail.html",
            {
                "cluster": cluster,
                "pods": pods,
                "nodes": nodes,
                "ingresses": ingress,
            }
        )


class ClusterSyncView(View):
    def get(self, request, *args, **kwargs):
        cluster = Cluster.objects.get(pk=kwargs["pk"])
        cluster.sync()
        return HttpResponseRedirect(reverse("cluster_detail", args=[cluster.pk]))


class PodDetailView(View):
    def get(self, request, *args, **kwargs):
        cluster = Cluster.objects.get(pk=kwargs["cluster_pk"])
        # pod = cluster.pod_set.get(pk=kwargs["pk"])
        pod = None

        return render(
            request,
            "k8smanager/pod_detail.html",
            {
                "cluster": cluster,
                "pod": pod,
            }
        )
