FROM python:3.8

COPY src ./app/src
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY queries ./queries
COPY alembic ./alembic
COPY alembic.ini alembic.ini
CMD python src/main.py