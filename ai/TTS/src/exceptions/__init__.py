from fastapi import HTTPException, status

UnauthorizedError = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Bad username or password")

TryRetryAfterError = HTTPException(
    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    detail="Извините, сервер временно недоступен, попробуйте попозже.")


ForbiddenError = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You have been denied access")

ServerError = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Sorry...")

WrongDataError = HTTPException(
    status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail="wrong data")

TokenExpiredError = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Token expired")

ForbiddenError = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You have been denied access")


def return_bad_request(massage: str) -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=massage)


def return_fail(massage: str) -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=massage)
