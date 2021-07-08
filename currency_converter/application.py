import os
from typing import Any

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from flask import Flask

from .models import db, ma
from .scheduler import sched
from .tasks import fetch_exchange_rate
import datetime
from .api import api
from .utils import CustomJsonEncoder


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://docker:secret@192.168.0.104:5432/converter_db",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SCHEDULER_API_ENABLED = True
    RESTFUL_JSON = {"cls": CustomJsonEncoder}
    DEBUG = True


import time


def create_app() -> Flask:
    # os.environ.setdefault("TZ", "Europe/Moscow")
    # time.tzset()
    app = Flask(__name__)
    app.json_encoder = CustomJsonEncoder
    app.config.from_object(Config())
    app.config.update(
        {
            "SCHEDULER_JOBSTORES": {
                "default": SQLAlchemyJobStore(
                    app.config["SQLALCHEMY_DATABASE_URI"]
                )
            }
        }
    )
    app.secret_key = os.urandom(40)
    db.init_app(app)
    db.create_all(app=app)
    ma.init_app(app)
    api.init_app(app)
    sched.init_app(app)
    sched.start()
    # запускаем задание при старте и в 00:00:59
    sched.add_job(
        fetch_exchange_rate.__name__,
        fetch_exchange_rate,
        trigger="cron",
        hour=0,
        minute=0,
        second=59,
        replace_existing=True,
        max_instances=1,
        next_run_time=datetime.datetime.now(),
    )
    return app
