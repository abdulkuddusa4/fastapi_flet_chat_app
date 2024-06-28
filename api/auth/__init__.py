from typing import Annotated

from fastapi import APIRouter, Request, WebSocket, Depends, Header, status
from fastapi.responses import JSONResponse

from api.auth.decorators import authenticate, auth, authenticate_websocket
from api.auth.dependencies import authenticate_user
from api.auth.models import User
from api.auth.schemas import RegisterPayload
from api.auth.service import AuthService
from api.common.helpers.request_parsers import get_json_key_or_raise_400


async def mf():
    print(".......")
    pass


router = APIRouter()
auth_service = AuthService()


@router.post(
    '/register',
    # dependencies=[Depends(authenticate_user)]
)
async def register(request: Request):
    # return mf()

    full_name, email, password = get_json_key_or_raise_400(
        await request.json(),
        required=['full_name', 'email', 'password']
    )
    return await auth_service.register(full_name, email, password)
    pass


@router.post('/login')
async def login(request: Request):
    email, password = get_json_key_or_raise_400(
        await request.json(),
        required=['email', 'password']
    )
    token = await auth_service.login(email, password)
    return JSONResponse(
        content={
            "msg": "login successful",
            "token": token
        },
        status_code=status.HTTP_200_OK,
        headers={
            "Authorization": token
        }
    )


@router.post('/valid')
async def get(request: Request, user: Annotated[User, Depends(authenticate_user)]):
    print(user)
    return "success"
    pass


async def get_token(Authorization: Annotated[str, Header()]):
    # print(Authorization)
    return Authorization

@router.post('/profile')
async def get_profile(request: Request, user: Annotated[User, Depends(authenticate_user)]):
    return JSONResponse(
        user.dict(include={'full_name', 'email'}),
        status_code=status.HTTP_200_OK
    )


@router.websocket('/chat')
# @authenticate_websocket
async def chat(websocket: WebSocket, user: Annotated[str, Depends(authenticate_user)]):
    # websocket = WebSocket()
    print(user)
    await websocket.accept()
    await websocket.send_text("good night")
    await websocket.receive()
    await websocket.close()
