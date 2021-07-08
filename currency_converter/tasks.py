import requests
from bs4 import BeautifulSoup
from .scheduler import sched
from sqlalchemy.dialects.postgresql import insert
from .models import ExchangeRate, db
from sqlalchemy.dialects import postgresql


def fetch_exchange_rate() -> None:
    app = sched.app
    with app.app_context():
        while True:
            try:
                r = requests.get("https://www.cbr.ru/scripts/XML_daily.asp")
                r.raise_for_status()
                bs = BeautifulSoup(r.text, "lxml")
                rates = []
                for v in bs.find_all("valute"):
                    code = v.find("charcode").text
                    # name = v.find("name").text
                    nominal = int(v.find("nominal").text)
                    value = (
                        float(v.find("value").text.replace(",", ".")) / nominal
                    )
                    rates.append(dict(code=code, value=value))
                app.logger.debug(rates)
                stmt = insert(ExchangeRate).values(rates)
                stmt = stmt.on_conflict_do_update(
                    constraint="exchange_rate_code_key",
                    set_={
                        "value": stmt.excluded.value,
                    },
                )
                app.logger.debug(stmt.compile(dialect=postgresql.dialect()))
                db.session.execute(stmt)
                break
            except Exception as e:
                app.logger.exception(e)
