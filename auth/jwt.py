from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError


SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"


def create_token(username: str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    payload = {
        "sub": username,
        "exp": expire
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token