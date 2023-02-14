import pytest
from rest_framework.test import APIClient
from . import models


@pytest.mark.django_db
def test_api_graph_details_404():
    api_client = APIClient()
    response = api_client.get("/api/graphs/1/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_api_graph_details():
    api_client = APIClient()
    graph = models.Graph.objects.create(
        name="TestGraph",
        type=models.GRAPHTYPE_BAR
    )
    response = api_client.get(f"/api/graphs/{graph.id}/")
    assert response.status_code == 200
