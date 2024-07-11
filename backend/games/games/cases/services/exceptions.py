from rest_framework.exceptions import APIException


class ChancesValuesError(APIException):
    default_detail = "Not correct chances of items drop in case"
