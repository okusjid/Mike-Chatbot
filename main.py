from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.router import api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Matt GPT", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"], #[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api_router)
