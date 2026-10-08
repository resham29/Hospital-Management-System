from fastapi import Request
from fastapi.responses import JSONResponse
from jose import jwt, JWTError

from auth.jwt import SECRET_KEY, ALGORITHM


async def verify_token(request: Request, call_next):

    public_paths = [
        "/login",
        "/docs",
        "/openapi.json",
        "/redoc"
    ]

    if request.url.path in public_paths:
        return await call_next(request)

    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return JSONResponse(
            status_code=401,
            content={"detail": "Authorization header missing"}
        )

    parts = auth_header.split(" ")

    if len(parts) != 2 or parts[0].lower() != "bearer":
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid Authorization header"}
        )

    token = parts[1]

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if not username:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid token"}
            )

        request.state.username = username

    except JWTError:
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid or expired token"}
        )

    return await call_next(request)