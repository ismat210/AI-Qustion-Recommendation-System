# backend/tests/tests.py

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


# ======================================================
# TEST 1: Upload API
# ======================================================
def test_upload_file():
    with open("sample_questions.pdf", "rb") as f:
        response = client.post(
            "/upload",
            files={"file": ("sample_questions.pdf", f, "application/pdf")}
        )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

    # 🔥 NEW CHECKS
    assert "question" in data[0]
    assert "topic" in data[0]
    assert "source" in data[0]


# ======================================================
# TEST 2: Processing Pipeline (direct test)
# ======================================================
def test_processing_pipeline():
    from backend.preprocessing.preprocessing import process_file_pipeline

    result = process_file_pipeline("sample_questions.pdf")

    assert isinstance(result, list)
    assert len(result) > 0

    for item in result:
        assert "question" in item
        assert "topic" in item
        assert "source" in item


# ======================================================
# TEST 3: Recommendation API
# ======================================================
def test_recommend():
    response = client.get("/recommend?query=what is machine learning")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    if len(data) > 0:
        assert isinstance(data[0], str)


# ======================================================
# TEST 4: Topic Tagger
# ======================================================
def test_topic_tagger():
    from backend.ml.topic_tagger import TopicTagger

    tagger = TopicTagger()

    topic = tagger.predict("What is neural network?")

    assert isinstance(topic, str)
    assert len(topic) > 0


# ======================================================
# TEST 5: Model Recommendation
# ======================================================
def test_model_recommendation():
    from backend.ml.model import HybridRecommender

    questions = [
        "what is machine learning?",
        "define artificial intelligence",
        "solve quadratic equation",
        "what is integration"
    ]

    model = HybridRecommender()
    model.train(questions)

    results = model.recommend("what is AI", top_k=2)

    assert isinstance(results, list)
    assert len(results) == 2


# ======================================================
# TEST 6: Edge Case (Empty Query)
# ======================================================
def test_empty_query():
    response = client.get("/recommend?query=")

    assert response.status_code in [200, 400]