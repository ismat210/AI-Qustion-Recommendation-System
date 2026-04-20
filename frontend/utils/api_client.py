import requests
import os

# ======================================================
# BASE URL (ENVIRONMENT FRIENDLY)
# ======================================================
BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


# ======================================================
# UPLOAD FILE (FULL PIPELINE)
# ======================================================
def upload_file(file):
    try:
        response = requests.post(
            f"{BASE_URL}/upload/",
            files={"file": file}
        )
        return response.json()

    except Exception as e:
        return {"error": str(e)}


# ======================================================
# RECOMMEND QUESTIONS
# ======================================================
def recommend(query, top_k=5):
    try:
        response = requests.get(
            f"{BASE_URL}/recommend/",
            params={
                "query": query,
                "top_k": top_k
            }
        )
        return response.json()

    except Exception as e:
        return {"error": str(e)}