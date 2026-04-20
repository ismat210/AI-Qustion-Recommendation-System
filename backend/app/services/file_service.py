import os
import shutil
import json
from datetime import datetime
import uuid
import joblib


# ======================================================
# BASE PATH
# ======================================================
BASE_PATH = os.path.join("backend", "data")

RAW_DIR = os.path.join(BASE_PATH, "raw")
PROCESSED_DIR = os.path.join(BASE_PATH, "processed")
MODEL_DIR = os.path.join(BASE_PATH, "models")


# ensure folders exist
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)


# ======================================================
# SAVE RAW FILE
# ======================================================
def save_raw_file(file, filename):

    unique_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex}_{filename}"
    path = os.path.join(RAW_DIR, unique_name)

    try:
        with open(path, "wb") as buffer:
            shutil.copyfileobj(file, buffer)
    except Exception as e:
        raise Exception(f"Failed to save file: {str(e)}")

    return path


# ======================================================
# SAVE PROCESSED DATA
# ======================================================
def save_processed(data, filename):

    name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
    path = os.path.join(PROCESSED_DIR, name)

    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    return {
        "path": path,
        "count": len(data)
    }


# ======================================================
# SAVE MODEL (VERSIONED)
# ======================================================
def save_model_file(model, name=None):

    if name is None:
        name = f"model_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"

    path = os.path.join(MODEL_DIR, name)

    joblib.dump(model, path)

    return path


# ======================================================
# GET LATEST MODEL
# ======================================================
def get_latest_model_path():

    if not os.path.exists(MODEL_DIR):
        return None

    files = [f for f in os.listdir(MODEL_DIR) if f.endswith(".pkl")]

    if not files:
        return None

    files.sort(
        key=lambda x: os.path.getmtime(os.path.join(MODEL_DIR, x)),
        reverse=True
    )

    return os.path.join(MODEL_DIR, files[0])