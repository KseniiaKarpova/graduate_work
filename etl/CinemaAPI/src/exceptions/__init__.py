from http import HTTPStatus

from fastapi import HTTPException

GenresNotFoundError = HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Genres Not Found")
GenreNotFoundError = HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Genre Not Found")

FilmsNotFoundError = HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Films Not Found")
FilmNotFoundError = HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Films Not Found")

PersonNotFoundError = HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Person Not Found")
PersonsNotFoundError = HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Persons Not Found")

FileNotFoundError = HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="File Not Found")
ForbiddenError = HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="You have been denied access")
ServerError = HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="ooops")
