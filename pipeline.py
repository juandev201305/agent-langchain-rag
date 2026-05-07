from formatter import format_docs
from prompts import *
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from config import *


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
