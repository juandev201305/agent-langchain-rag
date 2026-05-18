from services.llm_planner import build_plan
from utils.context_builder import build_context
from rag.retriever import initialize_retriever
from pipelines.unified_pipeline import execute_plan
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from prompts.synthesizer_prompt import SYNTHESIZER_PROMPT

# Ejecuta el flujo principal del agent
def run_agent(query:str, llm) -> dict:
    plan = build_plan(query=query, llm=llm)

    retriever = None

    needs_rag = any(
        step.tool == "rag"
        for step in plan.steps
    )

    if needs_rag:
        retriever = initialize_retriever()
    
    state = execute_plan(
        plan=plan,
        query=query,
        retriever=retriever,
        llm_model=llm
    )

    final_context = build_context(web_context=state["web_context"], rag_context=state["rag_context"])

    prompt = PromptTemplate.from_template(
        SYNTHESIZER_PROMPT
    )


    final_chain = (
        prompt
        | llm
        | StrOutputParser()
    )

    response = final_chain.invoke({
        "context": final_context,
        "query": query
    })

    return {
        "response": response,
        "plan": plan,
        "state": state
    }

