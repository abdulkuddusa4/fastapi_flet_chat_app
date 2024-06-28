import os

import jwt
from fastapi import Request, status as HTTP_STATUS, WebSocket, WebSocketException, HTTPException
from sqlmodel import Session, select

from api.auth.models import User
from api.common.db.sql import engine


async def auth(f):
    return f


def authenticate(f):
    async def decorated_route(request: WebSocket, *args, **kwargs):
        # MOCK A USER FOR TEST PURPOSE
        # END MOCK CODE SECTION
        # Extract JWT token from the Authorization header
        # is_coroutine =
        # print("decorator")
        # with Session(engine) as session:
        #     return await f(request)
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            raise HTTPException(
                HTTP_STATUS.HTTP_401_UNAUTHORIZED,
                f"Authorization header required"
            )

        try:
            # Check if the token is in the correct format (Bearer <token>)
            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != 'bearer':
                raise WebSocketException(HTTP_STATUS.HTTP_401_UNAUTHORIZED, 'Invalid token format')

            token = parts[1]  # Extract the token
            # Decode JWT token
            payload = jwt.decode(token, os.environ.get('AUTH_SECRET'), algorithms=['HS256'])
            email = payload['email']

            # Perform authorization check
            with Session(engine) as session:
                user = session.exec(select(User).where(User.email == email)).first()
            if user:
                # Authorized user, call the protected route function
                return await f(request, user)
            else:
                # Unauthorized user, return an error response
                raise HTTPException(HTTP_STATUS.HTTP_401_UNAUTHORIZED, "unauthorized user")

        except jwt.ExpiredSignatureError:
            raise HTTPException(HTTP_STATUS.HTTP_401_UNAUTHORIZED, "unauthorized user")
        except jwt.InvalidTokenError:
            raise HTTPException(HTTP_STATUS.HTTP_401_UNAUTHORIZED, "unauthorized user")

    return decorated_route


def authenticate_websocket(f):

    async def decorated_route(websocket: WebSocket):
        # MOCK A USER FOR TEST PURPOSE
        # END MOCK CODE SECTION
        # Extract JWT token from the Authorization header
        # is_coroutine =
        # print("decorator")
        # with Session(engine) as session:
        #     session.
        #     return await f(websocket)
        print("<<<<<<<<<<<<,")
        # return await f(websocket, "sdf")
        auth_header = websocket.headers.get('Authorization')

        if not auth_header:
            raise WebSocketException(
                HTTP_STATUS.WS_1008_POLICY_VIOLATION,
            )
        print("sfdsf")
        try:
            # Check if the token is in the correct format (Bearer <token>)
            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != 'bearer':
                raise HTTPException(HTTP_STATUS.HTTP_401_UNAUTHORIZED, 'Invalid token format')

            token = parts[1]  # Extract the token
            # Decode JWT token
            payload = jwt.decode(token, os.environ.get('AUTH_SECRET'), algorithms=['HS256'])
            email = payload['email']

            # Perform authorization check
            with Session(engine) as session:
                user = session.exec(select(User).where(User.email == email)).first()
            if user:
                # Authorized user, call the protected route function
                return await f(websocket, user)
            else:
                # Unauthorized user, return an error response
                raise HTTPException(HTTP_STATUS.HTTP_401_UNAUTHORIZED, "unauthorized user")

        except jwt.ExpiredSignatureError:
            raise HTTPException(HTTP_STATUS.HTTP_401_UNAUTHORIZED, "unauthorized user")
        except jwt.InvalidTokenError:
            raise HTTPException(HTTP_STATUS.HTTP_401_UNAUTHORIZED, "unauthorized user")

    return decorated_route

