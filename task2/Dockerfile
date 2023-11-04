FROM python:3.10

RUN pip install fastapi uvicorn[all]
RUN pip install sqlalchemy

COPY . /app
WORKDIR /app
EXPOSE 8000

CMD uvicorn app:app --host 0.0.0.0

