# backend/ml/evaluate.py

import random
import numpy as np
from backend.ml.topic_tagger import TopicTagger


# =====================================================
# 1. TOP-K EVALUATION
# =====================================================
def evaluate_topk(model, questions, k=5, sample_size=20):
    """
    Checks if original query appears in top-K results
    """

    if not questions:
        return 0.0

    sample_size = min(sample_size, len(questions))
    samples = random.sample(questions, sample_size)

    hits = 0

    for q in samples:
        try:
            results = model.recommend(q, top_k=k)

            if q in results:
                hits += 1
        except:
            continue

    return hits / sample_size


# =====================================================
# 2. TOPIC CONSISTENCY
# =====================================================
def evaluate_topic_consistency(model, questions, k=5, sample_size=20):
    """
    Checks if recommended questions match same topic
    """

    if not questions:
        return 0.0

    tagger = TopicTagger()

    sample_size = min(sample_size, len(questions))
    samples = random.sample(questions, sample_size)

    correct = 0

    for q in samples:
        try:
            query_topic = tagger.predict(q)
            results = model.recommend(q, top_k=k)

            for r in results:
                if tagger.predict(r) == query_topic:
                    correct += 1
                    break
        except:
            continue

    return correct / sample_size


# =====================================================
# 3. FINAL EVALUATION WRAPPER
# =====================================================
def evaluate(model, questions):
    """
    Returns clean dictionary of metrics
    """

    print("\n🔍 Evaluating model...")

    topk = evaluate_topk(model, questions)
    topic = evaluate_topic_consistency(model, questions)

    print(f"Top-K Accuracy: {topk:.3f}")
    print(f"Topic Consistency: {topic:.3f}")

    return {
        "topk_accuracy": topk,
        "topic_consistency": topic
    }


# =====================================================
# 4. FINAL SINGLE SCORE (USED FOR MODEL SELECTION)
# =====================================================
def final_score(metrics: dict):
    """
    Converts metrics → single comparable score
    """

    return 0.6 * metrics["topk_accuracy"] + 0.4 * metrics["topic_consistency"]