# backend/ml/model.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np
import joblib
from backend.ml.topic_tagger import TopicTagger


# =====================================================
# BASE RECOMMENDER
# =====================================================
class BaseRecommender:
    def train(self, questions):
        pass

    def recommend(self, query, top_k=5):
        pass


# =====================================================
# 1. TF-IDF RECOMMENDER (fast baseline)
# =====================================================
class TfidfRecommender(BaseRecommender):
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = None
        self.questions = None

    def train(self, questions):
        self.questions = questions
        self.matrix = self.vectorizer.fit_transform(questions)

    def recommend(self, query, top_k=5):
        q_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(q_vec, self.matrix)[0]

        idx = np.argsort(scores)[::-1][:top_k]
        return [self.questions[i] for i in idx]


# =====================================================
# 2. BERT / TRANSFORMER RECOMMENDER (semantic search)
# =====================================================
class BertRecommender(BaseRecommender):
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.embeddings = None
        self.questions = None

    def train(self, questions):
        self.questions = questions
        self.embeddings = self.model.encode(questions, show_progress_bar=True)

    def recommend(self, query, top_k=5):
        q_emb = self.model.encode([query])
        scores = cosine_similarity(q_emb, self.embeddings)[0]

        idx = np.argsort(scores)[::-1][:top_k]
        return [self.questions[i] for i in idx]


# =====================================================
# 3. HYBRID RECOMMENDER (BEST PERFORMANCE)
# =====================================================
class HybridRecommender(BaseRecommender):
    def __init__(self, use_topic_filter=True):
        self.tfidf = TfidfRecommender()
        self.bert = BertRecommender()
        self.questions = None

        # 🔥 Topic tagging integration
        self.topic_tagger = TopicTagger()
        self.use_topic_filter = use_topic_filter

    # -------------------------------------------------
    def train(self, questions):
        self.questions = questions
        self.tfidf.train(questions)
        self.bert.train(questions)

    # -------------------------------------------------
    # Topic filtering step (IMPORTANT upgrade)
    # -------------------------------------------------
    def _filter_by_topic(self, query, questions):
        if not self.use_topic_filter:
            return questions

        try:
            query_topic = self.topic_tagger.predict(query)

            filtered = [
                q for q in questions
                if self.topic_tagger.predict(q) == query_topic
            ]

            # fallback if empty
            return filtered if len(filtered) > 0 else questions

        except Exception:
            return questions

    # -------------------------------------------------
    def recommend(self, query, top_k=5):

        # STEP 1: topic filtering
        filtered_questions = self._filter_by_topic(query, self.questions)

        # STEP 2: TF-IDF similarity
        tfidf_scores = cosine_similarity(
            self.tfidf.vectorizer.transform([query]),
            self.tfidf.vectorizer.transform(filtered_questions)
        )[0]

        # STEP 3: BERT similarity
        query_emb = self.bert.model.encode([query])
        filtered_emb = self.bert.model.encode(filtered_questions)

        bert_scores = cosine_similarity(query_emb, filtered_emb)[0]

        # STEP 4: combine scores
        final_scores = (0.4 * tfidf_scores) + (0.6 * bert_scores)

        # STEP 5: rank results
        idx = np.argsort(final_scores)[::-1][:top_k]

        return [filtered_questions[i] for i in idx]


# =====================================================
# 4. OPTIONAL: SAVE / LOAD MODEL
# =====================================================
def save_model(model, path):
    joblib.dump(model, path)


def load_model(path):
    return joblib.load(path)