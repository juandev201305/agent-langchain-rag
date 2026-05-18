from config.settings import TAVILY_API_KEY
from tavily import TavilyClient

client = TavilyClient(
    api_key=TAVILY_API_KEY
)

# Función que realiza una busqueda web usando TavilyClient
def web_search(query:str):

    response = client.search(
        query=query,
        search_depth="advanced",
        max_results= 5
    )

    return response["results"]