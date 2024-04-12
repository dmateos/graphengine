from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView
from .models import UniversalTag, AWSAccessDetails, AzureAccessDetails


class IndexView(TemplateView):
    template_name = "tagman/index.html"


class TagListView(ListView):
    model = UniversalTag
    template_name = "tagman/tag_list.html"


class TagDetailView(View):
    def get(self, request, *args, **kwargs):
        tag = UniversalTag.objects.get(pk=kwargs["pk"])
        aws_auth = AWSAccessDetails.objects.first()
        azure_auth = AzureAccessDetails.objects.first()
        schedules = tag.schedules.all()

        if aws_auth:
            aws_vms = tag.get_aws_vms_with_tag(aws_auth)
        else:
            aws_vms = []

        if azure_auth:
            azure_vms = tag.get_azure_vms_with_tag(azure_auth)
        else:
            azure_vms = []

        return render(
            request,
            "tagman/tag_detail.html",
            {
                "tag": tag,
                "aws_vms": aws_vms,
                "azure_vms": azure_vms,
                "schedules": schedules,
            }
        )
