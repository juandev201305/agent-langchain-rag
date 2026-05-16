from formatter import format_docs
from prompts import *
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from config import *
from schemas.docx import DocumentModel
from services.docx_generator import generate_docx
from services.web_search import web_search

# Funcion para ejecutar RAG y obtener la respuesta del llm
def rag_chain(query, retriever, llm_model):
    llm = ChatOpenAI(model=llm_model, temperature = 0, openai_api_base=OPENROUTER_API)
    docs = retriever.invoke(query)

    context = format_docs(docs)
    
    print(context)
    print(query)

    prompt = PromptTemplate.from_template(
        CHAT_PROMPT
    )
    rag_chain= (
        prompt
        | llm
        | StrOutputParser()
    )
    
    response = rag_chain.invoke({
        "context": context,
        "question": query
    })
    return response


def generator_chain(query, llm_model):
    llm = ChatOpenAI(model=llm_model, temperature = 0, openai_api_base=OPENROUTER_API)

    llm_docx_generator = llm.with_structured_output(DocumentModel)

    prompt = PromptTemplate.from_template(
        DOCX_PROMPT
    )

    chain = (
        prompt
        | llm_docx_generator
    )
    
    result = chain.invoke({
        "query": query
    })

    file_path = generate_docx(doc_model=result, path="documento.docx")
    
    return file_path
    
def web_search_chain(query, llm_model):
    llm = ChatOpenAI(model=llm_model, temperature = 0, openai_api_base=OPENROUTER_API)

    results = web_search(query=query)

    results_formmated = "\n\n".join(
        [
            f"Título: {r['title']}\nURL: {r['url']}\nContenido: {r.get('content', '')}"
            for r in results
        ]
    )
    prompt = PromptTemplate.from_template(
        WEB_SEARCH_PROMPT
    )

    chain = (
        prompt
        | llm
        | StrOutputParser()
    )

    response = chain.invoke({
        "question": query,
        "search_results": results_formmated
    })

    return response