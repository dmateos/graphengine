from django.db import models
from django.db.models import F, FloatField
from django.db.models.functions import Cast
from pgvector.django import VectorField, HnswIndex, CosineDistance
from transformers import AutoTokenizer, AutoModel
import torch


class File(models.Model):
    embedding = VectorField(
        dimensions=384,
        help_text="Vector embeddings",
        null=True,
        blank=True,
    )
    text_data = models.TextField()

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

    def save_embedding(self, embedding):
        self.embedding = embedding.tolist()
        self.save()

    @staticmethod
    def encode_embedding(data):
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModel.from_pretrained(model_name)

        inputs = tokenizer(data, return_tensors="pt", padding=True, truncation=True)

        with torch.no_grad():
            outputs = model(**inputs)

        embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
        return embeddings

    @staticmethod
    def search_embedding(text):
        encoded = File.encode_embedding(text)
        files_with_distance = File.objects.annotate(
            distance=CosineDistance("embedding", encoded)
        ).order_by("distance")[:12]
        print(files_with_distance)
        return files_with_distance
