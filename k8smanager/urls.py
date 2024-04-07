from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("clusters/", views.ClusterListView.as_view(), name="clusters"),
    path(
        "clusters/<int:pk>/", views.ClusterDetailView.as_view(), name="cluster_detail"
    ),
    path(
        "clusters/<int:cluster_pk>/pods/<int:pk>/",
        views.PodDetailView.as_view(),
        name="pod_detail",
    ),
    path(
        "clusters/<int:pk>/sync/", views.ClusterSyncView.as_view(), name="cluster_sync"
    ),
]
