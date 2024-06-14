FROM python:latest

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY extract_from_db.py .
COPY load_to_s3.py .
COPY extract_load_pipeline.py .

CMD python3 extract_load_pipeline.py
