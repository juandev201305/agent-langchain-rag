from config.settings import TAVILY_API_KEY
from tavily import TavilyClient
from config.web import SEARCH_DEPTH, MAX_RESULTS

client = TavilyClient(
    api_key=TAVILY_API_KEY
)

# Realiza una busqueda web usando TavilyClient
def web_search(query:str) -> list[dict]:
    try:
        response = client.search(
            query=query,
            search_depth=SEARCH_DEPTH,
            max_results= MAX_RESULTS
        )
    except Exception as error:
        print(f"Error web search: {error}")
    return response["results"]