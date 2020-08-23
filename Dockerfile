FROM python:3.8
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY src ./src
COPY alembic ./alembic
COPY alembic.ini alembic.ini
CMD python src/main.py