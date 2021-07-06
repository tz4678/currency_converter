import requests
from bs4 import BeautifulSoup
from .scheduler import sched
from sqlalchemy.dialects.postgresql import insert
from .models import ExchangeRate, db
from sqlalchemy.dialects import postgresql


def fetch_exchange_rate() -> None:
    app = sched.app
    with app.app_context():
        for _ in range(3, 0, -1):
            try:
                r = requests.get("https://www.cbr.ru/scripts/XML_daily.asp")
                r.raise_for_status()
                bs = BeautifulSoup(r.text, "lxml")
                values = []
                for v in bs.find_all("valute"):
                    code = v.find("charcode").text
                    name = v.find("name").text
                    nominal = v.find("nominal").text
                    value = v.find("value").text.replace(",", ".")
                    values.append(
                        dict(code=code, name=name, nominal=nominal, value=value)
                    )
                app.logger.debug(values)
                stmt = insert(ExchangeRate).values(values)
                stmt = stmt.on_conflict_do_update(
                    constraint="exchange_rate_code_key",
                    set_={
                        "value": stmt.excluded.value,
                        "nominal": stmt.excluded.nominal,
                        "name": stmt.excluded.name,
                    },
                )
                app.logger.debug(stmt.compile(dialect=postgresql.dialect()))
                db.session.execute(stmt)
                break
            except requests.exceptions.HTTPError as e:
                app.logger.exception(e)
