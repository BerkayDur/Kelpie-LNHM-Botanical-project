FROM public.ecr.aws/lambda/python:latest

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY extract_from_db.py .
COPY load_to_s3.py .
COPY main.py .

CMD [ "main.handler" ]
