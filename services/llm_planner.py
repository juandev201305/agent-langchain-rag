from langchain_core.prompts import PromptTemplate
from schemas.step import Plan
from services.llm_factory import get_llm
from prompts.planner_prompt import PLANNER_PROMPT

# Genera un plan de ejecución según la intención del usuario
def build_plan(query: str, llm) -> Plan:
    if not query.strip():
        raise ValueError("Query is required")

    planner_llm = llm.with_structured_output(Plan)
    prompt = PromptTemplate.from_template(
        PLANNER_PROMPT
    )

    chain = (
        prompt
        | planner_llm
    )

    try:
        plan = chain.invoke({
            "query": query
        })
        return plan
    except Exception as e:
        raise RuntimeError("Error generatin plan") from e

   