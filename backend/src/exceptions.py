from fastapi import HTTPException
from starlette import status


class UserNotFoundException(HTTPException):
    def __init__(self, detail="User not found."):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class UserNotActiveException(HTTPException):
    def __init__(self, detail="User not active."):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class UserAuthenticationException(HTTPException):
    def __init__(self, detail="Invalid login or password."):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class NotMatchPasswordException(HTTPException):
    def __init__(self, detail="Password does not match."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class NotActiveUserException(HTTPException):
    def __init__(self, detail="User not active."):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class InvalidTokenException(HTTPException):
    def __init__(self, detail="Invalid token or expired."):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class InvalidTokenTypeException(HTTPException):
    def __init__(self, detail="Invalid token type."):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class TagNotFoundException(HTTPException):
    def __init__(self, detail="Tag not found."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class TagAlreadyExistsException(HTTPException):
    def __init__(self, detail="Tag already exists."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class NoteNotFoundException(HTTPException):
    def __init__(self, detail="Note not found."):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
