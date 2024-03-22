from fastapi import APIRouter, Request

from schemas.chat import ChatRequest, ChatResponse
from services.assistant import OpenAIGpt
from fastapi.templating import Jinja2Templates

api_router = APIRouter()
gpt = OpenAIGpt()
templates = Jinja2Templates(directory="templates")

@api_router.post("/chat")
async def chat(data: ChatRequest):
    try:
        response = await gpt.generate(data.email, data.message)
        return ChatResponse(message=response)
    except Exception as e:
        print(e)
        return "An error occurred while processing your request. Please try again later."
    
@api_router.get("/")
async def root(request: Request):
    return {"message": "Server is running!"}

@api_router.get("/chat")
async def get_chat_template(request: Request):
    return templates.TemplateResponse(
        request=request, name="chat.html"
    )
