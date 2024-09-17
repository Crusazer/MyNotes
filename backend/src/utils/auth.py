from datetime import datetime, timezone, timedelta

import bcrypt
import jwt

from src.config import settings


def encode_jwt(
        payload: dict,
        secret_key: str = settings.SECRET_KEY,
        algorithm: str = "HS256",
        expire_minutes: int = settings.ACCESS_TOKEN_LIFE,
) -> str:
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(exp=expire, iat=now)
    encoded = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded


def decode_jwt(
        token: str | bytes,
        secret_key: str = settings.SECRET_KEY,
        algorithm: str = "HS256",
) -> dict:
    decoded = jwt.decode(token, secret_key, algorithms=[algorithm])
    return decoded


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    password_bytes: bytes = password.encode()
    return bcrypt.hashpw(password=password_bytes, salt=salt).decode()


def validate_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password=password.encode(), hashed_password=hashed_password.encode()
    )
