from fastapi import APIRouter, UploadFile, File
import os
import shutil

from backend.app.utils.logger import logger
from backend.app.utils.exception import ProcessingException

from backend.preprocessing.preprocessing import process_file_pipeline
from backend.db.db_service import insert_questions


router = APIRouter()

UPLOAD_DIR = "backend/data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/")
async def process_file(file: UploadFile = File(...)):
    """
    Upload → save → process → store in DB
    """

    try:
        logger.info(f"Processing started: {file.filename}")

        # -------------------------------------------------
        # 1. Save uploaded file
        # -------------------------------------------------
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # -------------------------------------------------
        # 2. Run preprocessing pipeline
        # -------------------------------------------------
        json_data = process_file_pipeline(file_path)

        # -------------------------------------------------
        # 3. Save to database
        # -------------------------------------------------
        insert_questions(json_data)

        logger.info(f"Processing completed: {len(json_data)} questions saved")

        return {
            "status": "success",
            "questions_saved": len(json_data),
            "file": file.filename
        }

    except Exception as e:
        logger.exception("Processing failed")
        raise ProcessingException(str(e))