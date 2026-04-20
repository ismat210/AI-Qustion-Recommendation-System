from fastapi import FastAPI
from backend.app.api import upload, process, recommend

from backend.db.database import init_db
from backend.app.utils.logger import logger

import os


# ======================================================
# INIT APP
# ======================================================
app = FastAPI(
    title="AI Question Recommendation System",
    version="1.0"
)


# ======================================================
# STARTUP EVENT (VERY IMPORTANT)
# ======================================================
@app.on_event("startup")
def startup_event():
    logger.info("Starting backend...")

    # 1. Initialize database
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"DB init failed: {e}")

    # 2. Ensure data folders exist
    os.makedirs("backend/data/uploads", exist_ok=True)
    os.makedirs("backend/data/raw", exist_ok=True)
    os.makedirs("backend/data/processed", exist_ok=True)
    os.makedirs("backend/data/models", exist_ok=True)

    logger.info("Folders checked/created")


# ======================================================
# ROUTERS
# ======================================================
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(process.router, prefix="/process", tags=["Process"])
app.include_router(recommend.router, prefix="/recommend", tags=["Recommend"])


# ======================================================
# HEALTH CHECK (FOR DEPLOYMENT)
# ======================================================
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "Backend is healthy 🚀"
    }


# ======================================================
# ROOT
# ======================================================
@app.get("/")
def home():
    return {
        "message": "AI Question Recommendation System is running 🚀"
    }