FROM python:3.11-alpine AS builder

WORKDIR /app

RUN python3 -m venv venv
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY . .
RUN pip install -r requirements.txt

ENV FLASK_APP=app/main.py
ENV AMBIENTE=PROD

EXPOSE 8000




CMD [ "uvicorn", "--host", "0.0.0.0", "main:app" ]
