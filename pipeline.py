from formatter import format_docs
from prompts import *
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from config import *
from schemas.docx import DocumentModel
from services.docx_generator import generate_docx

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
    