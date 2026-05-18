from services.docx_generator import generate_docx
from langchain_core.prompts import PromptTemplate
from schemas.docx import DocumentModel
from prompts.docx_prompt import DOCX_PROMPT

# Genera la estructura del documento usando salida tipada del LLM
def run_pipeline_generator_docx(context, llm):

    llm_docx_generator = llm.with_structured_output(
        DocumentModel
    )

    prompt = PromptTemplate.from_template(
        DOCX_PROMPT
    )

    chain = (
        prompt
        | llm_docx_generator
    )

    document_model = chain.invoke({
        "context": context
    })

    return document_model
