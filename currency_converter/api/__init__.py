from flask_restful import Resource, Api, abort
from ..models import ExchangeRate, ExchangeRateSchema
from decimal import Decimal


class CustomApi(Api):
    pass
    # def handle_error(self, e: Exception) -> None:
    #     abort(e.code, str(e))


api = CustomApi()


class ExchangeRateList(Resource):
    def get(self) -> list[dict]:
        data = ExchangeRate.query.all()
        return ExchangeRateSchema().dump(data, many=True)


class ConvertToRUB(Resource):
    def get(self, from_code: str, quantity: float) -> dict[str, float]:
        if (
            rate := ExchangeRate.query.filter_by(code=from_code).first()
        ) is None:
            abort(400, message=f"Unknown currency code: {from_code!r}")
        return {
            "value": Decimal(quantity) / rate.nominal * rate.value,
            "code": "RUB",
        }


class ConvertFromRUB(Resource):
    def get(self, to_code: str, quantity: float) -> dict[str, float]:
        if (rate := ExchangeRate.query.filter_by(code=to_code).first()) is None:
            abort(400, message=f"Unknown currency code: {to_code!r}")
        return {
            "value": Decimal(quantity) / (rate.nominal * rate.value),
            "code": to_code,
        }


api.add_resource(ExchangeRateList, "/rates")
api.add_resource(ConvertToRUB, "/convert/<from_code>/RUB/<quantity>")
api.add_resource(ConvertFromRUB, "/convert/RUB/<to_code>/<quantity>")
