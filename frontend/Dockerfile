FROM python:3.12-slim
WORKDIR /app
COPY frontend/requirements.txt .
RUN pip install -r requirements.txt
COPY frontend/ .
CMD ["streamlit", "run", "frontend.py", "--server.port=8501"]