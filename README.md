Сервис раз в сутки обновляет базу с сайта ЦБ России.

Данный сервис должен использоваться в микросервисной архитектуре. Можно было бы напрямую обращаться к API ЦБ, но тогда будет довольно высокая латентность + колмчество запросов с определенного IP может ограничиваться.

```bash
# Список всех обменных курсов
$ http :8000/rates
HTTP/1.0 200 OK
Content-Length: 2850
Content-Type: application/json
Date: Tue, 06 Jul 2021 20:38:02 GMT
Server: Werkzeug/2.0.1 Python/3.9.6

[
    {
        "code": "CNY",
        "nominal": 1,
        "value": 11.3362
    },
    ...
]

# Когда вспоминаешь, что когда-то доллар стоил 27-30 рублей, то сразу вспоминаешь о тои как Россия «встала» с колен
$ http :8000/convert/RUB/USD/10000
HTTP/1.0 200 OK
Content-Length: 54
Content-Type: application/json
Date: Tue, 06 Jul 2021 20:40:04 GMT
Server: Werkzeug/2.0.1 Python/3.9.6

{
    "code": "RUB",
    "value": 136.4889580432943
}

# Но пока есть зимбабвийские доллары и казахские тугрики рублю есть куда падать
$ http :8000/convert/KZT/RUB/1000
HTTP/1.0 200 OK
Content-Length: 44
Content-Type: application/json
Date: Tue, 06 Jul 2021 20:40:45 GMT
Server: Werkzeug/2.0.1 Python/3.9.6

{
    "code": "RUB",
    "value": 171.823
}

# Если добавлялись новые зависимости
$ poetry export -f requirements.txt > req

# Создаем образ
$ docker build -t currency-converter .

# Создаем и запускаем контейнер
$ docker run -d -p 8000:8000 -it currency-converter
```
