from services.web_search import web_search

# Recupera y formatea resultados de búsqueda web
def run_pipeline_web_search(query) -> str:
    results = web_search(query=query)

    results_formatted = "\n\n".join(
        [
            f"Título: {r['title']}\nURL: {r['url']}\nContenido: {r.get('content', '')}"
            for r in results
        ]
    )

    return results_formatted