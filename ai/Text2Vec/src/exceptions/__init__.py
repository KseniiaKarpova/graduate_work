from fastapi import HTTPException, status

UnauthorizedError = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Bad username or password")

ServerError = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Sorry...")

ForbiddenError = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You have been denied access")

Created = HTTPException(
    status_code=status.HTTP_201_CREATED,
    detail="Data has been created")

IncorrectCredentialsError = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="incorrect login or password")

Ok = HTTPException(
    status_code=status.HTTP_200_OK,
    detail="User has been updated")

NotFoundError = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Not found")

TryRetryError = HTTPException(
    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    detail="Извините, сервер временно недоступен, попробуйте попозже.")

EmptyError = HTTPException(
    status_code=status.HTTP_204_NO_CONTENT,
    detail="Not found")


def return_bad_request(massage: str) -> HTTPException:
    HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=massage)


def return_fail(massage: str) -> HTTPException:
    HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=massage)
