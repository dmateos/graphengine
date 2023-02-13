from django.db import models

GRAPHTYPE_LINE = "line"
GRAPHTYPE_BAR = "bar"


class Graph(models.Model):
    name = models.CharField(max_length=32, null=False)
    type = models.CharField(max_length=16, null=False, default=GRAPHTYPE_LINE, choices=(
        (GRAPHTYPE_LINE, "line"),
        (GRAPHTYPE_BAR, "bar"),
    ))

    def get_points(self):
        data = [float(n.data) for n in self.graphpoint_set.all()]
        return data

    def get_labels(self):
        label = [n.label for n in self.graphpoint_set.all()]
        return label

    def create_point(self, label, data):
        try:
            new_seq = self.graphpoint_set.all().order_by("-sequence").first().sequence+1
        except AttributeError:
            new_seq = 0

        return GraphPoint.objects.create(
            graph=self,
            label=label,
            data=data,
            sequence=new_seq,
        )

    def get_latest(self, sequence_id):
        data = self.graphpoint_set.filter(sequence__gt=sequence_id)
        return [float(n.data) for n in data]


class GraphPoint(models.Model):
    data = models.CharField(max_length=32, null=False)
    label = models.CharField(max_length=8, default=0, null=False)
    graph = models.ForeignKey(Graph, on_delete=models.CASCADE, null=False)

    created = models.DateTimeField(auto_now=True)
    sequence = models.IntegerField(default=0, null=False)
