import pytest
from . import models


def create_test_graph():
    return models.Graph.objects.create(
        name="TestGraph",
        type=models.GRAPHTYPE_BAR
    )


@pytest.mark.django_db
def test_graph_sequence_logic():
    graph = create_test_graph()

    for _ in range(0, 5):
        graph.create_point("", 0)

    sequence = graph.get_from_sequence(2)
    assert len(sequence) == 2


@pytest.mark.django_db
def test_graph_sequence_incrementing():
    graph = create_test_graph()

    for n in range(0, 5):
        g = graph.create_point("", 0)
        assert g.sequence == n


@pytest.mark.django_db
def test_graph_get_all_points():
    graph = create_test_graph()
    for n in range(0, 5):
        graph.create_point("", n)

    points = graph.get_points()
    assert points == [0, 1, 2, 3, 4]


@pytest.mark.django_db
def test_graph_get_all_labels():
    graph = create_test_graph()
    graph.create_point("test1", 0)
    graph.create_point("test2", 0)

    points = graph.get_labels()
    assert points == ["test1", "test2"]
