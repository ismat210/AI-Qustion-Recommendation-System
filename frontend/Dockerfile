FROM python:3.11-slim

WORKDIR /app

COPY frontend /app/frontend
COPY pyproject.toml uv.lock /app/

RUN pip install uv && uv sync

CMD ["streamlit", "run", "frontend/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]