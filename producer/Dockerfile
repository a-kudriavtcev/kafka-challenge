FROM python:3.12

COPY producer /

RUN pip install --no-cache-dir -r /requirements.txt

CMD ["python3", "/producer.py"]
