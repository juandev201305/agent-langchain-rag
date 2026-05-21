from tools.registry import TOOLS
from schemas.step import Plan
from services.docx_generator import generate_docx


# Ejecuta un plan de steps y orquesta las tools necesarias
def execute_plan(
    plan: Plan,
    query: str,
    retriever=None,
    llm_model=None,
):
    
    # Estado compartido entre los pasos del pipeline
    state = {
        "query": query,
        "web_context": None,
        "rag_context": None,
        "document_model": None,
        "document_id": None,
    }

    # Ejecuta cada step definido en el plan
    for step in plan.steps:

        # Obtiene contexto desde búsqueda web
        if step.tool == "web":
            state["web_context"] = TOOLS["web"](
                query=query
            )

        # Obtiene contexto desde RAG
        elif step.tool == "rag":
            state["rag_context"] = TOOLS["rag"](
                query=query,
                retriever=retriever
            )

        # Genera documento usando el contexto acumulado
        elif step.tool == "document":

            # Combina contexto web + RAG ignorando valores None
            combined_context = "\n\n".join(
                filter(None, [
                    state["web_context"],
                    state["rag_context"]
                ])
            )

            # Genera estructura del documento
            state["document_model"] = TOOLS["document"](
                context=combined_context,
                llm=llm_model
            )

            # Exporta el documento a formato .docx
            state["document_id"] = generate_docx(
                doc_model=state["document_model"]
            )
            print(state["document_id"])

    return state