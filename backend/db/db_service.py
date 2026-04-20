# backend/db/db_service.py

from backend.db.database import get_connection
from backend.app.utils.logger import logger


# ======================================================
# INSERT QUESTIONS
# ======================================================
def insert_questions(question_list):

    conn = get_connection()
    cursor = conn.cursor()

    inserted = 0
    skipped = 0

    for q in question_list:

        question = q.get("question")

        # 🔥 skip invalid
        if not question or len(question.strip()) < 5:
            skipped += 1
            continue

        try:
            cursor.execute("""
            INSERT OR IGNORE INTO questions (question, topic, source_file, difficulty)
            VALUES (?, ?, ?, ?)
            """, (
                question.strip(),
                q.get("topic"),
                q.get("source"),
                q.get("difficulty")
            ))

            if cursor.rowcount > 0:
                inserted += 1
            else:
                skipped += 1

        except Exception as e:
            logger.warning(f"Skipping bad record: {e}")
            skipped += 1

    conn.commit()
    conn.close()

    logger.info(f"Inserted: {inserted}, Skipped: {skipped}")


# ======================================================
# FETCH ALL QUESTIONS
# ======================================================
def fetch_all_questions():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT question FROM questions WHERE question IS NOT NULL")
    rows = cursor.fetchall()

    conn.close()

    return [r[0] for r in rows]


# ======================================================
# FETCH QUESTIONS WITH TOPIC
# ======================================================
def fetch_questions_with_topic():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT question, topic 
        FROM questions 
        WHERE question IS NOT NULL
    """)
    rows = cursor.fetchall()

    conn.close()

    return [
        {"question": r[0], "topic": r[1]}
        for r in rows
    ]