# backend/ml/topic_tagger.py

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity


class TopicTagger:

    def __init__(self, questions=None, n_clusters=5):

        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.k = n_clusters

        if questions:
            self._fit(questions)
        else:
            self.kmeans = None
            self.centroids = None

    # -------------------------------------------------
    # Train clustering model
    # -------------------------------------------------
    def _fit(self, questions):

        embeddings = self.model.encode(questions)

        self.kmeans = KMeans(n_clusters=self.k, random_state=42)
        self.kmeans.fit(embeddings)

        self.centroids = self.kmeans.cluster_centers_

    # -------------------------------------------------
    # Predict topic (cluster id)
    # -------------------------------------------------
    def predict(self, text):

        if self.centroids is None:
            return "Unknown"

        emb = self.model.encode([text])

        sims = cosine_similarity(emb, self.centroids)[0]

        cluster_id = int(np.argmax(sims))

        return f"Topic_{cluster_id}"

    # -------------------------------------------------
    # Batch prediction
    # -------------------------------------------------
    def predict_batch(self, texts):

        results = []

        for t in texts:
            results.append(self.predict(t))

        return results