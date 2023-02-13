from rest_framework.test import APIClient


def test_api_test():
    api_client = APIClient()
    response = api_client.get("/api/graph")
    assert response.status_code == 404
