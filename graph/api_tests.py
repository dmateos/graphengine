import pytest
import json

from rest_framework.test import APIClient
from . import models


@pytest.mark.django_db
def test_api_graph_get_404():
    api_client = APIClient()
    response = api_client.get("graphs/api/graphs/1/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_api_graph_get():
    api_client = APIClient()
    graph = models.Graph.objects.create(name="TestGraph", type=models.GRAPHTYPE_BAR)
    response = api_client.get(f"/graphs/api/graphs/{graph.id}/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_api_graphpoints_get():
    api_client = APIClient()
    graph = models.Graph.objects.create(name="TestGraph", type=models.GRAPHTYPE_BAR)
    graph.create_point("test point", 0)
    response = api_client.get(f"/graphs/api/graphpoints/{graph.id}/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_api_graphpoints_get_404():
    api_client = APIClient()
    response = api_client.get("/graphs/api/graphpoints/1/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_api_graphpoints_get_from_sequence():
    api_client = APIClient()
    graph = models.Graph.objects.create(name="TestGraph", type=models.GRAPHTYPE_BAR)
    for n in range(0, 5):
        graph.create_point(n, n)

    response = api_client.get("/graphs/api/graphpoints/?sequence=2")
    assert response.status_code == 200

    response_parsed = json.loads(response.content)
    print(response_parsed)
    assert len(response_parsed) == 2


@pytest.mark.django_db
def test_api_graphpoints_filter_by_graph():
    api_client = APIClient()
    graph1 = models.Graph.objects.create(name="TestGraph", type=models.GRAPHTYPE_BAR)
    graph1.create_point("", "")
    graph1.create_point("", "")
    graph2 = models.Graph.objects.create(name="TestGraph", type=models.GRAPHTYPE_BAR)
    graph2.create_point("", "")
    graph2.create_point("", "")

    response = api_client.get("/graphs/api/graphpoints/?graph=1")
    assert response.status_code == 200

    response_parsed = json.loads(response.content)
    assert len(response_parsed) == 2


@pytest.mark.django_db
def test_api_graphpoints_push():
    pass


@pytest.mark.django_db
def test_api_graphpoints_push_increases_sequence():
    pass
