from fastapi import HTTPException, status

unauthorized = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Bad username or password")

try_retry_after = HTTPException(
    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    detail="Извините, сервер временно недоступен, попробуйте попозже.")


forbidden_error = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You have been denied access")

server_error = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Sorry...")

wrong_data = HTTPException(
    status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail="wrong data")

def return_bad_request(massage: str) -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=massage)

def return_fail(massage: str) -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=massage)
