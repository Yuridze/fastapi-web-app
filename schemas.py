from pydantic import BaseModel

# Схема для создания пользователя (регистрация)
class UserCreate(BaseModel):
    username: str
    password: str

# Схема для ответа с данными пользователя
class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True  # Updated from orm_mode to from_attributes

# Схема для входа пользователя
class UserLogin(BaseModel):
    username: str
    password: str

# Схема для ответа с токеном
class Token(BaseModel):
    access_token: str
    token_type: str