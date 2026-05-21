from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import FRONTEND_URL

# Configurar middlewares globales
def setup_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            FRONTEND_URL
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )