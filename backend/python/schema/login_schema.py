from pydantic import BaseModel

class LoginRequestSchema(BaseModel):
    username: str
    password: str

class LoginResponseSchema(BaseModel):
    message: str
    session_id: str

class LogoutResponseSchema(BaseModel):
    message: str