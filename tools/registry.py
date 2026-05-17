from pipelines.rag_pipeline import run_pipeline_rag
from pipelines.web_pipeline import run_pipeline_web_search
from pipelines.generate_docx_pipeline import run_pipeline_generator_docx

# Registro central de tools disponibles para el pipeline unified
TOOLS = {
    "rag": run_pipeline_rag,
    "web": run_pipeline_web_search,
    "document": run_pipeline_generator_docx,
}
