import os
import uuid
from datetime import datetime, timedelta

import jwt

from api.auth.models import User
from api.common.db.sql import engine
from sqlmodel import Session, select, delete
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi import status


class AuthService:
    def __init__(self):
        self.db_session = Session(engine)
        self.auth_secret = os.environ.get('AUTH_SECRET')

    def _generate_jwt_token(self, email):
        # Set token expiration time
        expires = datetime.utcnow() + timedelta(hours=48)

        # Create payload
        payload = {
            'email': email,
            'exp': expires
        }

        # Generate JWT token
        token = jwt.encode(payload, self.auth_secret, algorithm='HS256')
        return token

    async def register(self, full_name, email, password):
        with self.db_session as session:
            user = session.exec(select(User).where(User.email == email)).first()
            if user:
                raise HTTPException(status.HTTP_409_CONFLICT, f"user {email} already exists")

            user = User(
                full_name=full_name,
                email=email
            )
            user.set_password(password)
            session.add(user)
            session.commit()
            return JSONResponse(f"account created for {email}", status.HTTP_200_OK)

    async def login(self, email, password):
        with self.db_session as session:
            user = session.exec(select(User).where(User.email == email)).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"user {email} not found"
            )

        if not user.check_password(password):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"invalid password for {email}"
            )
        return self._generate_jwt_token(email)


    def generate_password_reset_token(self, reset_form_url, user_id):
        if not (user_info := User.find_one_with_email(user_id)):
            return JSONResponse({
                "error": f"user {user_id} does'nt exists"
            }, 404)

        if not (password_alias := user_info.get('password_alias')):
            password_alias = str(uuid.uuid4())
            db.users.update_one(
                {"email": user_id},
                {"$set": {
                    "password_alias": password_alias
                }}
            )
            print(user_info)
            print(db.users.find_one({"email": user_id}))

        password_reset_secret = os.environ.get("JWT_SECRET_KEY")

        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(hours=1)
        }

        token = jwt.encode(payload, password_reset_secret + password_alias, algorithm='HS256')
        one_time_link = f"{reset_form_url}?token={token}"
        print("sending email...")
        done, _err = send_password_reset_mail(
            "Password Reset Link for Mazala-Ai",
            one_time_link,
            user_id,
            user_info.get('username')
        )
        if not done:
            return wrap_response({
                "error": _err
            }, 500)
        print("token: >>")
        print(one_time_link)
        print("<< :token")
        return wrap_response({
            "msg": "email sent"
        }, 200)

    def check_token_and_reset_password(self, user_id, token, new_password):
        if not (user_info := db.users.find_one({"email": user_id})):
            return wrap_response({
                "error": f"user {user_id} does'nt exists"
            }, 404)

        if not (password_alias := user_info.get('password_alias')):
            print(password_alias)
            password_alias = str(uuid.uuid4())
            return wrap_response({
                "error": "token integraty failed"
            }, 400)

        password_reset_secret = os.environ.get("JWT_SECRET_KEY")

        try:
            payload = jwt.decode(token, password_reset_secret + password_alias, algorithms=['HS256'])
            if payload['user_id'] != user_id:
                return wrap_response({
                    "error": f"the id {user_id} and the given token does'nt match"
                }, 401)

            db.users.update_one(
                {"email": user_id},
                {"$set": {
                    "password": new_password,
                    "password_alias": str(uuid.uuid4())
                }}
            )
            return wrap_response({
                "msg": "password reset successfully you can login with your new password"
            }, 200)
        except jwt.ExpiredSignatureError as e:
            return wrap_response({
                'error': 'token expired'
            }, 401)
        except jwt.InvalidTokenError as e:
            return wrap_response({
                "error": "invalid token"
            }, 401)



