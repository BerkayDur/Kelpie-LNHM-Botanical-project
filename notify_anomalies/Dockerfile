FROM public.ecr.aws/lambda/python:latest

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY calculate_anomalies.py .
COPY sns_alert.py .
COPY main.py .


CMD [ "main.handler" ]