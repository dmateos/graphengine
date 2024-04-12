from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView
from .models import UniversalTag


class IndexView(TemplateView):
    template_name = "tagman/index.html"


class TagListView(ListView):
    model = UniversalTag
    template_name = "tagman/tag_list.html"


class TagDetailView(View):
    def get(self, request, *args, **kwargs):
        tag = UniversalTag.objects.get(pk=kwargs["pk"])
        return render(
            request, "tagman/tag_detail.html", {"tag": tag}
        )
