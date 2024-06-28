import datetime

from pydantic import BaseModel, field_validator, ValidationError, model_validator


class RegisterPayload(BaseModel):
    full_name: str
    email: str
    password: str
