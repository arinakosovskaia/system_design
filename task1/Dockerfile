FROM python:3.10

RUN pip install fastapi uvicorn[all]

COPY app.py /app/app.py
EXPOSE 8000

WORKDIR /app
CMD uvicorn app:app --host 0.0.0.0

