FROM python:3.12-slim AS base

WORKDIR /app

RUN addgroup --system app && adduser --system --ingroup app app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

ENV PORT=8080
EXPOSE 8080

USER app

CMD ["gunicorn", "-b", "0.0.0.0:8080", "app.main:app"]
