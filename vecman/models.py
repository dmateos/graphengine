from django.db import models
from pgvector.django import VectorField, HnswIndex


class File(models.Model):
    embedding = VectorField(
        dimensions=768,
        help_text="Vector embeddings",
        null=True,
        blank=True,
    )

    class Meta:
        indexes = [
            HnswIndex(
                name="clip_l14_vectors_index",
                fields=["embedding"],
                m=16,
                ef_construction=64,
                opclasses=["vector_cosine_ops"],
            )
        ]
