from django.db import models
from django.db.models import F
from pgvector.django import VectorField, HnswIndex
from transformers import AutoTokenizer, AutoModel
import torch


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

    def encode_embedding(self, document):
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModel.from_pretrained(model_name)

        inputs = tokenizer(document, return_tensors="pt", padding=True, truncation=True)

        with torch.no_grad():
            outputs = model(**inputs)

        embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
        return embeddings

    def save_embedding(self, embedding):
        self.embedding = embedding.tolist()

    def search_embedding(self, text):
        encoded = self.encode_embedding(text)

        results = File.objects.annotate(
            distance=F("embedding").distance(encoded.tolist())
        ).order_by("distance")[:5]

        return results
