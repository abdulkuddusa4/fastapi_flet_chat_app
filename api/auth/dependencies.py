import os
from typing import Annotated

import jwt
from fastapi import Request, status as HTTP_STATUS, WebSocket, Header
from fastapi.exceptions import HTTPException
from sqlmodel import Session, select

from api.auth.models import User
from api.common.db.sql import engine


async def auth(f):
    return f


async def authenticate_user(Authorization: Annotated[str, Header()]):
    # MOCK A USER FOR TEST PURPOSE
    # END MOCK CODE SECTION
    # Extract JWT token from the Authorization header
    # is_coroutine =
    # print("decorator")
    # with Session(engine) as session:
    #     return session.exec(select(User)).first()
    #     return await f(websocket)
    auth_header = Authorization
    # print(headers)
    # return "nothing"
    # auth_header = headers.get('Authorization')

    if not auth_header:
        raise HTTPException(
            HTTP_STATUS.HTTP_401_UNAUTHORIZED,
            f"Authorization header required"
        )

    try:
        # Check if the token is in the correct format (Bearer <token>)
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            raise HTTPException(HTTP_STATUS.HTTP_401_UNAUTHORIZED, 'Invalid token format')

        token = parts[1]  # Extract the token
        # Decode JWT token
        print("decoding")
        payload = jwt.decode(token, os.environ.get('AUTH_SECRET'), algorithms=['HS256'])
        print("done")
        email = payload['email']

        # Perform authorization check
        with Session(engine) as session:
            user = session.exec(select(User).where(User.email == email)).first()
        if user:
            # Authorized user, call the protected route function
            return user
        else:
            # Unauthorized user, return an error response
            raise HTTPException(HTTP_STATUS.HTTP_401_UNAUTHORIZED, "unauthorized user")

    except jwt.ExpiredSignatureError:
        raise HTTPException(HTTP_STATUS.HTTP_401_UNAUTHORIZED, "unauthorized user")
    except jwt.InvalidTokenError:
        raise HTTPException(HTTP_STATUS.HTTP_401_UNAUTHORIZED, "invalid token")
