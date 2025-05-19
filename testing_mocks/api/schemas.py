from pydantic import BaseModel, field_validator
from typing import List, Dict, Optional

class UserCreate(BaseModel):
    username: str
    password: str

    @field_validator('password')
    def password_must_not_be_empty(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Пароль не может быть пустым')
        return v

class UserInDB(BaseModel):
    id: int
    username: str
    
    class Config:
        orm_mode = True

class UserFileInfo(BaseModel):
    id: int
    filename: str
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None