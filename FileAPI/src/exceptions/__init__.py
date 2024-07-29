from fastapi import HTTPException, status

FileNotFoundError = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File Not Found")
ServerError = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="sorry... some problem")
FileAlreadyExistError = HTTPException(status_code=status.HTTP_409_CONFLICT, detail="File with that name already exists")

UnauthorizedError = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Bad username or password")

WrongDataError = HTTPException(
    status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail="wrong data")

ServerError = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Sorry...")

ForbiddenError = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You have been denied access")

TokenExpiredError = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Token expired")

AlreadyExistsError = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Data already exists")

Deleted = HTTPException(
    status_code=status.HTTP_200_OK,
    detail="the record deleted")
