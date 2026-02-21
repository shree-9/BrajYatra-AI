"""
Semantic Agent — uses sentence-transformers and FAISS for
semantic search over the location database.
"""

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


class SemanticAgent:

    def __init__(self, locations):
        self.locations = locations
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # Build rich text for each location for better semantic matching
        texts = []
        for loc in locations:
            parts = [
                loc.get("name", ""),
                loc.get("category", ""),
                loc.get("description", ""),
                loc.get("location", {}).get("city", ""),
                " ".join(loc.get("embedding_metadata", {}).get("tags", [])),
                " ".join(loc.get("visitor_profile_fit", {}).get("recommended_for", []))
            ]
            texts.append(" ".join(parts))

        embeddings = self.model.encode(
            texts, convert_to_numpy=True
        ).astype("float32")

        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)

        print(f"[SemanticAgent] Indexed {len(locations)} locations ({dim}D embeddings).")

    def search(self, query, k=20):
        """
        Search for the top-k locations most semantically similar to the query.
        """
        k = min(k, len(self.locations))

        q_emb = self.model.encode(
            [query], convert_to_numpy=True
        ).astype("float32")

        distances, indices = self.index.search(q_emb, k)

        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.locations):
                loc = self.locations[idx].copy()
                loc["_semantic_distance"] = float(distances[0][i])
                results.append(loc)

        return results
