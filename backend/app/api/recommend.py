from fastapi import APIRouter
from backend.app.utils.logger import logger
from backend.app.utils.exception import ModelException
from backend.ml.model import load_model

router = APIRouter()

# ✔ correct path (VERY IMPORTANT)
model = load_model("backend/data/models/best_model.pkl")


@router.get("/")
def recommend(query: str):
    try:
        logger.info(f"Recommendation requested: {query}")

        results = model.recommend(query)

        # -------------------------------------------------
        # 🔥 REMOVE DUPLICATES HERE
        # -------------------------------------------------
        seen = set()
        unique_results = []

        for r in results:
            if r not in seen:
                unique_results.append(r)
                seen.add(r)

        results = unique_results

        return {
            "query": query,
            "results": results
        }

    except Exception as e:
        logger.exception("Recommendation failed")
        return {
            "results": [],
            "error": str(e)
        }