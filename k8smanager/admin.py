from django.contrib import admin
from .models import Cluster, Node, Pod, Ingress, Deployment, Service

admin.site.register(Cluster)
admin.site.register(Node)
admin.site.register(Pod)
admin.site.register(Ingress)
admin.site.register(Deployment)
admin.site.register(Service)
