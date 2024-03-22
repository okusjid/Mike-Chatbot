from pydantic import BaseModel, EmailStr

class ChatRequest(BaseModel):
    email: EmailStr
    message: str

class ChatResponse(BaseModel):
    message: str
