<<<<<<< HEAD
FROM python:3.11-
=======
FROM python:3.11-slim123
>>>>>>> 4b41b90 (test rebase)

WORKDIR /app

COPY requirements.txt .
<<<<<<< HEAD
RUN pip install --no-cache-dir -r requirements
=======
RUN pip install --no-cache-dir -r requirements.123
>>>>>>> 4b41b90 (test rebase)

COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]