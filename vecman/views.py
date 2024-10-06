from django.shortcuts import render
from django.views import View
from .models import File
from . import forms


class IndexView(View):
    def get(self, request):
        get = request.GET.get("input", None)
        form = forms.TextInputForm()

        if get:
            docs = File.search_embedding(get)
            return render(
                request,
                "vecman/index.html",
                {"documents": docs, "query": get, "form": form},
            )
        else:
            return render(request, "vecman/index.html", {"form": form})
