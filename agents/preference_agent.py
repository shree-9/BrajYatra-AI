"""
Preference Agent — builds user preference vectors using
sentence-transformers for personalized ranking.
"""

from sentence_transformers import SentenceTransformer
import numpy as np


class PreferenceAgent:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def build_user_vector(self, user_queries):
        """
        Build a user preference vector from their queries.

        Args:
            user_queries: list of strings (past queries, preferences)

        Returns:
            numpy array — mean embedding vector
        """

        if not user_queries:
            return None

        embeddings = self.model.encode(
            user_queries, convert_to_numpy=True
        )

        return np.mean(embeddings, axis=0)

    def similarity_score(self, user_vector, location):
        """
        Calculate how well a location matches user preferences.

        Args:
            user_vector: user's preference embedding
            location: location dict

        Returns:
            float similarity score (0 to 1)
        """

        if user_vector is None:
            return 0.5  # Neutral if no preference data

        # Build location text for embedding
        parts = [
            location.get("name", ""),
            location.get("category", ""),
            " ".join(location.get("embedding_metadata", {}).get("tags", [])),
            " ".join(location.get("visitor_profile_fit", {}).get("recommended_for", []))
        ]
        loc_text = " ".join(parts)

        loc_vector = self.model.encode([loc_text], convert_to_numpy=True)[0]

        # Cosine similarity
        dot = np.dot(user_vector, loc_vector)
        norm = np.linalg.norm(user_vector) * np.linalg.norm(loc_vector)

        if norm == 0:
            return 0.5

        return float(dot / norm)
