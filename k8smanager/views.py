from django.views.generic import TemplateView, ListView
from django.views import View
from .models import Cluster
from django.shortcuts import render


class IndexView(TemplateView):
    template_name = "k8smanager/index.html"


class ClusterListView(ListView):
    model = Cluster
    template_name = "k8smanager/cluster_list.html"


class ClusterDetailView(View):
    def get(self, request, *args, **kwargs):
        cluster = Cluster.objects.get(pk=kwargs["pk"])
        return render(
            request,
            "k8smanager/cluster_detail.html",
            {"cluster": cluster}
        )
