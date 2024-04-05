from django.contrib import admin
from .models import Cluster, Node, Pod

admin.site.register(Cluster)
admin.site.register(Node)
admin.site.register(Pod)
