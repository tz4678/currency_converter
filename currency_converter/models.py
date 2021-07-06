from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy(session_options={"autocommit": True})
ma = Marshmallow()


class ExchangeRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(3), unique=True)
    name = db.Column(db.String(255))
    nominal = db.Column(db.Integer)
    value = db.Column(db.Numeric(10, 4))


class ExchangeRateSchema(ma.Schema):
    class Meta:
        model = ExchangeRate
        fields = ("code", "nominal", "value")
