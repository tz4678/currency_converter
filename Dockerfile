FROM python:3.9.5-slim

WORKDIR /code
COPY . .

RUN pip install poetry && \
  poetry export -f requirements.txt | pip install -r /dev/stdin

CMD ["gunicorn", "-w", "8", "-b", "0.0.0.0:8000", "currency_converter:create_app"]
