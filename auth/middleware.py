from fastapi import Request
from fastapi.responses import JSONResponse
from jose import jwt, JWTError

from auth.jwt import SECRET_KEY, ALGORITHM

#read again
async def verify_token(request: Request, call_next):

    public_paths = [
        "/login",
        "/docs",
        "/openapi.json",
        "/redoc"
    ]

    if request.url.path in public_paths:
        return await call_next(request)
#check what is a header
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return JSONResponse(
            status_code=401,
            content={"detail": "Authorization header missing"}
        )
#explain .split() method in python
    parts = auth_header.split(" ")
#.lower() method in python
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid Authorization header"}
        )
# difference between = and == in python
    token = parts[1]
#try and catch block in python
    try:
        #how does encoding and decoding work in jwt
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
        #why di we set the username in request.state
        request.state.username = username

    except JWTError:
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid or expired token"}
        )
#what does call_next do and how does it work in fastapi
#return keyword in python
    return await call_next(request)