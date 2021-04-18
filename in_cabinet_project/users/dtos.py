from pydantic import BaseModel
from pydantic.networks import EmailStr
from pydantic.class_validators import validator

COMMON_PASSWORDS = [
    "123456",
    "123456789",
    "picture1",
    "password",
    "12345678",
    "111111",
    "123123",
    "12345",
    "1234567890",
    "senha",
]


class InvalidPassword(ValueError):
    message: str


class EasyPassword(InvalidPassword):
    message = "Senha muito usada."


class ShortPassword(InvalidPassword):
    message = "Senha muito curta. Mínimo: 8 caracteres"


class RegisterDTO(BaseModel):
    username: str
    first_name: str
    password: str
    last_name: str
    email: EmailStr
    password: str

    @validator("password")
    def password_validation(cls, value: str):
        if value in COMMON_PASSWORDS:
            raise EasyPassword
        if len(value) < 8:
            raise ShortPassword
        return value


class LoginDTO(BaseModel):
    username: str
    password: str