# backend/ml/dataset.py

import random
from backend.db.database import get_connection


class QuestionDataset:

    # -------------------------------------------------
    # Load all questions
    # -------------------------------------------------
    def load_questions(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT question FROM questions")
        rows = cursor.fetchall()

        conn.close()

        return [r[0] for r in rows]

    # -------------------------------------------------
    # 🔥 NEW: TRAIN / TEST SPLIT
    # -------------------------------------------------
    def train_test_split(self, test_size=0.2, shuffle=True):

        questions = self.load_questions()

        if len(questions) < 10:
            raise Exception("Need at least 10 questions for splitting")

        if shuffle:
            random.shuffle(questions)

        split_idx = int(len(questions) * (1 - test_size))

        train = questions[:split_idx]
        test = questions[split_idx:]

        return train, test