# backend/ml/train.py

from backend.ml.dataset import QuestionDataset
from backend.ml.model import (
    TfidfRecommender,
    BertRecommender,
    HybridRecommender
)
from backend.ml.evaluate import evaluate, final_score
from backend.ml.topic_tagger import TopicTagger
from backend.app.services.file_service import save_model_file

import logging

logger = logging.getLogger("train")


# ======================================================
# LOAD DATASET
# ======================================================
dataset = QuestionDataset()
questions = dataset.load_questions()

if not questions or len(questions) < 10:
    raise Exception(
        "Not enough questions. Please upload more data (at least 10+)."
    )


# ======================================================
# TRAIN / TEST SPLIT (CRITICAL FIX)
# ======================================================
train_questions, test_questions = dataset.train_test_split(test_size=0.2)

logger.info(f"Train size: {len(train_questions)}")
logger.info(f"Test size: {len(test_questions)}")


# ======================================================
# TRAIN TOPIC TAGGER (EMBEDDING CLUSTERING)
# ======================================================
logger.info("Training topic tagger (unsupervised)...")

topic_tagger = TopicTagger(train_questions)

logger.info("Topic tagger ready")


# ======================================================
# INIT MODELS
# ======================================================
models = {
    "tfidf": TfidfRecommender(),
    "bert": BertRecommender(),
    "hybrid": HybridRecommender()
}

scores = {}


# ======================================================
# TRAIN + EVALUATE
# ======================================================
for name, model in models.items():

    logger.info(f"\nTraining model: {name}")

    # train only on TRAIN data
    model.train(train_questions)

    # evaluate only on TEST data
    metrics = evaluate(model, test_questions)

    # final comparable score
    scores[name] = final_score(metrics)

    logger.info(
        f"{name} -> "
        f"TopK: {metrics['topk_accuracy']:.3f}, "
        f"Topic: {metrics['topic_consistency']:.3f}, "
        f"Final: {scores[name]:.3f}"
    )


# ======================================================
# SELECT BEST MODEL
# ======================================================
best_model_name = max(scores, key=scores.get)
best_model = models[best_model_name]

logger.info(f"\nBest model selected: {best_model_name}")


# ======================================================
# SAVE BEST MODEL
# ======================================================
model_path = save_model_file(best_model, "best_model.pkl")

logger.info(f"Model saved at: {model_path}")


# ======================================================
# OUTPUT SUMMARY
# ======================================================
print("\n==============================")
print("TRAINING COMPLETE")
print("==============================")
print(f"Train size: {len(train_questions)}")
print(f"Test size: {len(test_questions)}")
print("Scores:", scores)
print("Best Model:", best_model_name)
print("Saved At:", model_path)