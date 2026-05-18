# Construye contexto unificado para respuesta del agente
def build_context(web_context=None, rag_context=None):
    context = []

    if web_context:
        context.append(
            "=== WEB RESULTS ==="
        )

        context.append(
            web_context
        )

    if rag_context:
        context.append(
            "=== RAG RESULTS ==="
        )

        context.append(
            rag_context
        )

    return "\n\n".join(
        context
    )