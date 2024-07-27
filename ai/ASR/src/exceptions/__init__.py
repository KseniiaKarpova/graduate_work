from http import HTTPStatus
from core import settings
from fastapi import HTTPException, status

class_not_found = HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Class Not Found.")
server_error = HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Sorry... some error.")
file_error = HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                           detail=f"Sorry... but I cant read your file. Use wav file and sample_rate: {settings.basemodel.sample_rate}")
big_file = HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="your file is BIG")

incorrect_credentials = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="incorrect login or password")


not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Not found")

try_retry_after = HTTPException(
    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    detail="Извините, сервер временно недоступен, попробуйте попозже.")

empty = HTTPException(
    status_code=status.HTTP_204_NO_CONTENT,
    detail="Not found")
