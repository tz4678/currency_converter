FROM python:3.9.5-slim

WORKDIR /code
COPY . .

RUN pip install poetry && \
  poetry export -f requirements.txt | pip install -r /dev/stdin

CMD ["python", "-m", "currency_converter"]
