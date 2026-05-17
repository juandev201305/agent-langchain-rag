from typing import Literal, Optional
from pydantic import BaseModel


class Step(BaseModel):
    tool: Literal[
        "web",
        "rag",
        "document"
    ]
    input: Optional[str] = None


class Plan(BaseModel):
    steps: list[Step]