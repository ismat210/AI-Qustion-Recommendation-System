# backend/db/database.py

import sqlite3
import os
from datetime import datetime


# ======================================================
# PATH
# ======================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DB_DIR, "questions.db")


# ======================================================
# CONNECTION
# ======================================================
def get_connection():
    os.makedirs(DB_DIR, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    return conn


# ======================================================
# INIT DATABASE
# ======================================================
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL UNIQUE,
        source_file TEXT,
        topic TEXT,
        difficulty TEXT,
        created_at TEXT
    )
    """)

    # 🔥 index for fast lookup
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_topic ON questions(topic)")

    conn.commit()
    conn.close()


# ======================================================
# SAFE SINGLE INSERT
# ======================================================
def insert_question(question, topic=None, source_file=None, difficulty=None):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT OR IGNORE INTO questions
        (question, topic, source_file, difficulty, created_at)
        VALUES (?, ?, ?, ?, ?)
        """, (
            question.strip(),
            topic,
            source_file,
            difficulty,
            datetime.utcnow().isoformat()
        ))

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        conn.close()


# ======================================================
# SAFE BULK INSERT
# ======================================================
def insert_questions_bulk(data):

    conn = get_connection()
    cursor = conn.cursor()

    records = []

    for item in data:
        q = item.get("question")

        # skip bad data
        if not q or len(q.strip()) < 5:
            continue

        records.append((
            q.strip(),
            item.get("topic"),
            item.get("source"),
            item.get("difficulty"),
            datetime.utcnow().isoformat()
        ))

    try:
        cursor.executemany("""
        INSERT OR IGNORE INTO questions
        (question, topic, source_file, difficulty, created_at)
        VALUES (?, ?, ?, ?, ?)
        """, records)

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        conn.close()


# ======================================================
# FETCH ALL
# ======================================================
def get_all_questions():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM questions")
    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


# ======================================================
# FETCH BY TOPIC
# ======================================================
def get_questions_by_topic(topic):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM questions WHERE topic = ?
    """, (topic,))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


# ======================================================
# CLEAR DATABASE
# ======================================================
def clear_questions():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM questions")

    conn.commit()
    conn.close()