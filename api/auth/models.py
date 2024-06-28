import hashlib
import uuid

from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    __tablename__ = 'users'
    full_name: str
    email: str = Field(unique=True, primary_key=True)
    salt: str = Field(default_factory=lambda: str(uuid.uuid4()))
    digest: str = Field(default_factory=lambda: str(uuid.uuid4()))
    recover_alias: str = Field(default_factory=lambda: str(uuid.uuid4()))



    def set_password(self, password):
        self.digest = hashlib.sha3_256(f"{self.salt}{password}".encode()).hexdigest()

    def check_password(self, password):
        return hashlib.sha3_256(f"{self.salt}{password}".encode()).hexdigest() == self.digest
