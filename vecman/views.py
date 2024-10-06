from django.shortcuts import render
from django.views import View
from .models import File


class IndexView(View):
    def get(self, request):
        get = request.GET.get("get", None)

        if get:
            docs = File.search_embedding(get)
            return render(
                request, "vecman/index.html", {"documents": docs, "query": get}
            )
        else:
            return render(request, "vecman/index.html")
