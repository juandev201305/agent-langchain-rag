from fastapi import FastAPI

from api.controllers.agent_controller import router as agent_router 
from api.controllers.documents_controller import router as document_router
from api.middleware import setup_middlewares

app = FastAPI(
    title="Api Agent",
    version="1.0.0"
)

setup_middlewares(app)

app.include_router(
    agent_router,
    prefix="/api"
)
app.include_router(
    document_router,
    prefix="/api"
)