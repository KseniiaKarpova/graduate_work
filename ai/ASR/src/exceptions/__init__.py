from fastapi import HTTPException
from http import HTTPStatus

class_not_found = HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Class Not Found.")
server_error = HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Sorry... some error.")
file_error = HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Sorry... but I cant read your file.")