from fastapi import APIRouter, UploadFile, File
import os
import shutil

from backend.app.services.file_service import save_raw_file
from backend.app.utils.logger import logger
from backend.app.utils.exception import ProcessingException

from backend.preprocessing.preprocessing import process_file_pipeline
from backend.db.db_service import insert_questions


router = APIRouter()


@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload → save → process → store in DB
    """

    try:
        logger.info("Uploading file")

        # -------------------------------------------------
        # 1. Save file
        # -------------------------------------------------
        file_path = save_raw_file(file.file, file.filename)

        logger.info(f"File saved at: {file_path}")

        # -------------------------------------------------
        # 2. Run preprocessing pipeline
        # -------------------------------------------------
        json_data = process_file_pipeline(file_path)

        # -------------------------------------------------
        # 3. Store in DB
        # -------------------------------------------------
        insert_questions(json_data)

        logger.info(f"{len(json_data)} questions saved to DB")

        # -------------------------------------------------
        # 4. Return response
        # -------------------------------------------------
        return {
            "status": "success",
            "file": file.filename,
            "questions_extracted": len(json_data),
            "sample": json_data[:3]  # preview
        }

    except Exception as e:
        logger.exception("Upload failed")
        raise ProcessingException(str(e))