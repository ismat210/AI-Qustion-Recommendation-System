# backend/preprocessing/preprocessing.py

import os
import re
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import docx

from backend.app.utils.logger import logger
from backend.app.utils.exception import ProcessingException
from backend.ml.topic_tagger import TopicTagger


# ======================================================
# INIT TOPIC TAGGER (LOAD ONCE)
# ======================================================
try:
    tagger = TopicTagger()
except Exception as e:
    logger.warning(f"TopicTagger not loaded: {e}")
    tagger = None


# ======================================================
# MAIN PIPELINE FUNCTION
# ======================================================
def process_file_pipeline(file_path: str):
    """
    Full pipeline:
    file → text → clean → questions → topic tagging → JSON
    """
    try:
        logger.info(f"Processing file: {file_path}")

        raw_text = extract_text_from_file(file_path)
        cleaned_text = clean_text(raw_text)

        questions = extract_questions(cleaned_text)
        json_data = questions_to_json(questions, file_path)

        logger.info(f"Extracted {len(json_data)} questions")

        return json_data

    except Exception as e:
        logger.exception("Processing pipeline failed")
        raise ProcessingException(str(e))


# ======================================================
# FILE TYPE HANDLING
# ======================================================
def extract_text_from_file(file_path: str) -> str:
    ext = os.path.splitext(file_path)[-1].lower()

    if ext == ".pdf":
        return extract_pdf(file_path)

    elif ext in [".png", ".jpg", ".jpeg"]:
        return extract_image(file_path)

    elif ext == ".docx":
        return extract_docx(file_path)

    else:
        raise ProcessingException("Unsupported file type")


# ======================================================
# PDF EXTRACTION
# ======================================================
def extract_pdf(file_path: str) -> str:
    logger.info("Extracting PDF text")

    doc = fitz.open(file_path)
    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()
    return text


# ======================================================
# IMAGE OCR
# ======================================================
def extract_image(file_path: str) -> str:
    logger.info("Running OCR on image")

    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)

    return text


# ======================================================
# DOCX EXTRACTION
# ======================================================
def extract_docx(file_path: str) -> str:
    logger.info("Extracting DOCX text")

    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])

    return text


# ======================================================
# CLEANING (UPDATED)
# ======================================================
def clean_text(text: str) -> str:
    """
    Cleaner but keeps useful symbols for ML
    """
    text = text.lower()

    # keep ?, ., numbers, and math symbols
    text = re.sub(r'[^a-z0-9?.+\-*/=^ ]', ' ', text)

    text = re.sub(r'\s+', ' ', text).strip()
    return text


# ======================================================
# QUESTION EXTRACTION (IMPROVED)
# ======================================================
def extract_questions(text: str):
    """
    Extracts questions from text using:
    - punctuation
    - numbering patterns (1. 2. etc.)
    - keywords
    """

    # split by punctuation OR numbering
    sentences = re.split(r'(?<=[?.!])\s+|\d+\.\s+', text)

    questions = []

    for s in sentences:
        s = s.strip()

        if len(s) < 10:
            continue

        if (
            s.endswith("?") or
            s.startswith((
                "what", "why", "how", "when", "where",
                "define", "explain", "describe",
                "solve", "find", "calculate"
            ))
        ):
            questions.append(s)

    return list(set(questions))


# ======================================================
# JSON CONVERSION + TOPIC TAGGING
# ======================================================
def questions_to_json(questions, file_name):
    """
    Adds topic tagging + metadata
    """
    data = []

    for q in questions:
        try:
            if tagger:
                topic = tagger.predict(q)
            else:
                topic = "Unknown"
        except Exception:
            topic = "Unknown"

        data.append({
            "question": q,
            "topic": topic,   # 🔥 ML FEATURE
            "source": os.path.basename(file_name)
        })

    return data