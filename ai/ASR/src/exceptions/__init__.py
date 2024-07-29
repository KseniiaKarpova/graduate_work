from http import HTTPStatus
from core import settings
from fastapi import HTTPException, status

ClassNotFoundError = HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Class Not Found.")
ServerError = HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Sorry... some error.")
FileError = HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                 detail=f"Sorry... but I cant read your file.\
                                  Use WAV file and sample_rate:  {settings.core.valid_sample_rate}\
                                  , but recommended use {settings.core.recommended_sample_rate}")
BigFileError = HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="your file is BIG")

IncorrectCredentialsError = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="incorrect login or password")


NotFoundError = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Not found")

TryRetryAfterError = HTTPException(
    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    detail="Извините, сервер временно недоступен, попробуйте попозже.")

EmptyError = HTTPException(
    status_code=status.HTTP_204_NO_CONTENT,
    detail="Not found")
