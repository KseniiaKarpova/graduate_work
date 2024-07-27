from http import HTTPStatus
from core import settings
from fastapi import HTTPException, status

Error_class_not_found = HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Class Not Found.")
Error_server_error = HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Sorry... some error.")
Error_file_error = HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                 detail=f"Sorry... but I cant read your file.\
                                  Use WAV file and sample_rate:  {settings.core.valid_sample_rate}\
                                  , but recommended use {settings.core.recommended_sample_rate}")
Error_big_file = HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="your file is BIG")

Error_incorrect_credentials = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="incorrect login or password")


Error_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Not found")

Error_try_retry_after = HTTPException(
    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    detail="Извините, сервер временно недоступен, попробуйте попозже.")

Error_empty = HTTPException(
    status_code=status.HTTP_204_NO_CONTENT,
    detail="Not found")
