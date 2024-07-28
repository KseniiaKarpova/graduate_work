from fastapi import HTTPException, status

TokenExpiredError = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Token expired")

UnauthorizedError = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Bad username or password")

Created = HTTPException(
    status_code=status.HTTP_201_CREATED,
    detail="Data has been created")

BadReqIdError = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='X-Request-Id is required')

Ok = HTTPException(
    status_code=status.HTTP_200_OK,
    detail="User has been updated")

NotFoundError = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Not found")

TryRetryAfterError = HTTPException(
    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    detail="Извините, сервер временно недоступен, попробуйте попозже.")

ConfigFailError = HTTPException(
    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    detail="Извините, конфигурационный файл неверно настроен для интентов")

EmptyError = HTTPException(
    status_code=status.HTTP_204_NO_CONTENT,
    detail="Not found")

ForbiddenError = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You have been denied access")

ServerError = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Sorry...")

WrongDataError = HTTPException(
    status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail="wrong data")


def return_bad_request(massage: str) -> HTTPException:
    HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=massage)


def return_fail(massage: str) -> HTTPException:
    HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=massage)
