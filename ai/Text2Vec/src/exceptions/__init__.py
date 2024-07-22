from fastapi import HTTPException, status

unauthorized = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Bad username or password")

created = HTTPException(
    status_code=status.HTTP_201_CREATED,
    detail="Data has been created")

incorrect_credentials = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="incorrect login or password")

ok = HTTPException(
    status_code=status.HTTP_200_OK,
    detail="User has been updated")

not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Not found")

try_retry_after = HTTPException(
    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    detail="Извините, сервер временно недоступен, попробуйте попозже.")

empty = HTTPException(
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
