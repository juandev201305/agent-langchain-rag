from services.web_search import web_search

# Funcion que ejecuta pipeline que busca informacion por internet
def run_pipeline_web_search(query):
    results = web_search(query=query)

    results_formmated = "\n\n".join(
        [
            f"Título: {r['title']}\nURL: {r['url']}\nContenido: {r.get('content', '')}"
            for r in results
        ]
    )

    return results_formmated