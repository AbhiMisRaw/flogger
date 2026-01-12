from http import HTTPStatus
from django.http.response import JsonResponse


class Error:

    @staticmethod
    def send(data, status_code = HTTPStatus.BAD_REQUEST):
        res = {
            "type":"error",
            "message": data
        }
        return JsonResponse(
            data=res,
            safe=True,
            status=status_code
        )
    

class Succes:

    @staticmethod
    def send(data, status_code = HTTPStatus.OK):
        res = {
            "type":"succes",
            "data": data
        }
        return JsonResponse(
            data=res,
            safe=True,
            status=status_code,
        )