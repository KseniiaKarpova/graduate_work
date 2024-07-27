from fastapi import HTTPException, status

Error_token_expired = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Token expired")

Error_unauthorized = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Bad username or password")

Error_created = HTTPException(
    status_code=status.HTTP_201_CREATED,
    detail="Data has been created")

Error_bad_req_id = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='X-Request-Id is required')

Error_ok = HTTPException(
    status_code=status.HTTP_200_OK,
    detail="User has been updated")

Error_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Not found")

Error_try_retry_after = HTTPException(
    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    detail="Извините, сервер временно недоступен, попробуйте попозже.")

Error_config_fail = HTTPException(
    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    detail="Извините, конфигурационный файл неверно настроен для интентов")

Error_empty = HTTPException(
    status_code=status.HTTP_204_NO_CONTENT,
    detail="Not found")

Error_forbidden_error = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You have been denied access")

Error_server_error = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Sorry...")

Error_wrong_data = HTTPException(
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
