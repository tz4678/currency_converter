Сервис раз в сутки обновляет базу с сайта ЦБ России.

Данный сервис должен использоваться в микросервисной архитектуре. Можно было бы напрямую обращаться к API ЦБ, но тогда будет довольно высокая латентность + колмчество запросов с определенного IP может ограничиваться.

```bash
# Список всех обменных курсов
$ http ':8000/rates'
HTTP/1.0 200 OK
Content-Length: 2138
Content-Type: application/json
Date: Thu, 08 Jul 2021 12:41:13 GMT
Server: Werkzeug/2.0.1 Python/3.9.6

[
    {
        "code": "AUD",
        "value": 55.8776
    },
    {
        "code": "AZN",
        "value": 44.2585
    },
    {
        "code": "GBP",
        "value": 103.6115
    },
    ...
]

# Конвертируем из RUB в KZT
$ http ':8000/convert/KZT/1000'
HTTP/1.0 200 OK
Content-Length: 54
Content-Type: application/json
Date: Thu, 08 Jul 2021 12:40:19 GMT
Server: Werkzeug/2.0.1 Python/3.9.6

{
    "code": "KZT",
    "value": 5729.017473503295
}

# KZT в RUB
$ http ':8000/convert/KZT/1000?from=1'
HTTP/1.0 200 OK
Content-Length: 55
Content-Type: application/json
Date: Thu, 08 Jul 2021 12:39:52 GMT
Server: Werkzeug/2.0.1 Python/3.9.6

{
    "code": "RUB",
    "value": 174.54999999999998
}

# Создаем образ
$ docker build -t currency-converter .

# Создаем и запускаем контейнер
$ docker run -d -p 8000:8000 -it currency-converter
```
