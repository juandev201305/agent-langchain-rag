from fastapi import APIRouter, HTTPException
from api.schemas.chat_request import ChatRequest
from api.schemas.chat_response import ChatResponse
from services.agent import run_agent
from services.llm_factory import get_llm

router = APIRouter()

# Endpoint que ejecuta el flujo principal del agente
@router.post("/chat")
def chat(request: ChatRequest) -> ChatResponse:
    
    try:
        llm = get_llm(request.model)
        result = run_agent(query=request.query, llm=llm)

        return ChatResponse(
            response= result["response"],
            plan=result["plan"].model_dump(),
            document_generated=result["state"].get("document_id") is not None,
            document_id=result["state"].get("document_id")
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


