from flask_restful import Resource, Api, abort, reqparse
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


class Converter(Resource):
    def get(self, code: str, quantity: str) -> dict[str, float]:
        if (rate := ExchangeRate.query.filter_by(code=code).first()) is None:
            abort(400, message=f"Unknown currency code: {code!r}")

        parser = reqparse.RequestParser()
        parser.add_argument("from", default=False, type=bool)
        args = parser.parse_args()
        print(args)

        quantity = float(quantity)

        return (
            {"value": quantity * rate.value, "code": "RUB"}
            if args["from"]
            else {"value": quantity / rate.value, "code": code}
        )


api.add_resource(ExchangeRateList, "/rates")
api.add_resource(Converter, "/convert/<code>/<quantity>")
