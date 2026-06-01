# Agente Inteligente con RAG, Búsqueda Web y Generación de Documentos

Sistema de agente inteligente basado en modelos de lenguaje de gran escala (LLM) que integra recuperación aumentada por generación (RAG), búsqueda web en tiempo real y generación estructurada de documentos. El agente planifica y ejecuta flujos de trabajo multi-paso de forma autónoma, seleccionando las herramientas adecuadas según la intención de cada consulta del usuario.

---

## Objetivos

- Implementar un agente con capacidad de planificación autónoma que seleccione entre múltiples herramientas según la naturaleza de la consulta.
- Integrar un sistema RAG que permita indexar y consultar documentos PDF y DOCX mediante una base de datos vectorial local.
- Incorporar búsqueda web en tiempo real para complementar el conocimiento del modelo con información actualizada.
- Generar documentos estructurados (DOCX) a partir del contexto combinado de fuentes internas y externas.
- Exponer todas las funcionalidades a través de una API REST documentada y una interfaz web interactiva.

---

## Tecnologías y herramientas

### Backend (Python)

| Categoría | Tecnología |
|---|---|
| Framework API | FastAPI + Uvicorn |
| Orquestación LLM | LangChain |
| Modelos de lenguaje | OpenRouter (Llama 4 Maverick, Gemini 2.5 Flash Lite, Qwen 3.5 Flash, DeepSeek V4) |
| Modelo de embeddings | `qwen/qwen3-embedding-8b` vía OpenRouter |
| Base de datos vectorial | ChromaDB (persistencia local) |
| Búsqueda web | Tavily Search API |
| Carga de documentos | PyPDF, docx2txt |
| Generación de documentos | python-docx |
| Validación de datos | Pydantic |

---

## Estructura del proyecto

```
langchain_chatbot/
├── .env                          # Variables de entorno (API keys)
├── requirements.txt              # Dependencias de Python
├── api/                          # Capa de API REST (FastAPI)
│   ├── main.py                   # Punto de entrada de la aplicación
│   ├── middleware.py              # Configuración de CORS
│   ├── controllers/
│   │   ├── agent_controller.py   # Endpoint /api/chat
│   │   └── documents_controller.py # Endpoints de gestión documental
│   └── schemas/
│       ├── chat_request.py       # Esquema de solicitud de chat
│       └── chat_response.py      # Esquema de respuesta de chat
├── config/                       # Configuración del sistema
│   ├── settings.py               # Variables de entorno y constantes
│   ├── models.py                 # Modelos LLM y embeddings disponibles
│   ├── retriever.py              # Parámetros del recuperador RAG
│   └── web.py                    # Parámetros de búsqueda web
├── pipelines/                    # Pipelines de ejecución de herramientas
│   ├── unified_pipeline.py       # Orquestador del plan de ejecución
│   ├── rag_pipeline.py           # Pipeline de consulta RAG
│   ├── web_pipeline.py           # Pipeline de búsqueda web
│   └── generate_docx_pipeline.py # Pipeline de generación de documentos
├── prompts/                      # Plantillas de prompts del sistema
│   ├── planner_prompt.py         # Prompt para planificación del agente
│   ├── synthesizer_prompt.py     # Prompt para síntesis de respuesta final
│   ├── rag_prompt.py             # Prompt para consulta sobre documentos
│   ├── web_prompt.py             # Prompt para síntesis de resultados web
│   └── docx_prompt.py            # Prompt para generación de documentos
├── rag/                          # Sistema RAG
│   ├── document_loader.py        # Carga de archivos PDF y DOCX
│   ├── chunker.py                # División de documentos en fragmentos
│   ├── vector_store.py           # Gestión de la base de datos vectorial
│   └── retriever.py              # Configuración del recuperador
├── schemas/                      # Modelos de datos estructurados
│   ├── step.py                   # Paso y plan de ejecución
│   ├── docx.py                   # Estructura de documento generado
│   └── generated_document.py     # Documento en memoria
├── services/                     # Lógica de negocio
│   ├── agent.py                  # Orquestador principal del agente
│   ├── llm_factory.py            # Fábrica de instancias LLM
│   ├── llm_planner.py            # Planificador basado en LLM
│   ├── document_service.py       # Servicio de gestión documental
│   ├── document_store.py         # Almacenamiento en memoria de documentos
│   ├── docx_generator.py         # Generador de archivos DOCX
│   ├── embeddings.py             # Proveedor de embeddings
│   └── web_search.py             # Cliente de búsqueda web Tavily
├── tools/                        # Registro de herramientas del agente
│   └── registry.py               # Mapeo de nombres a funciones
├── utils/                        # Utilidades
│   ├── context_builder.py        # Constructor de contexto combinado
│   └── formatter.py              # Formateador de fragmentos recuperados
├── chroma_db/                    # Base de datos vectorial (autogenerada)

```

---

## Instalación y configuración

### Requisitos previos

- Python 3.10 o superior
- Node.js 18 o superior
- Una clave API de [OpenRouter](https://openrouter.ai/)
- Una clave API de [Tavily](https://tavily.com/)

### Backend

```bash
# Clonar el repositorio
git clone https://github.com/juandev201305/agent-langchain-rag.git
cd langchain_chatbot

# Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate      # Linux / macOS
# venv\Scripts\activate       # Windows

# Instalar dependencias
pip install -r requirements.txt
```

Crear un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
OPENAI_API_KEY=sk-or-v1-tu_clave_de_openrouter
TAVILY_API_KEY=tvly-dev-tu_clave_de_tavily
```

## Ejecución

### Iniciar el servidor API

```bash
# Desde la raíz del proyecto, con el entorno virtual activado
uvicorn api.main:app --reload --port 8000
```

La API estará disponible en `http://localhost:8000`. La documentación interactiva (Swagger UI) se encuentra en `http://localhost:8000/docs`.

### Endpoints principales

| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/api/chat` | Enviar consulta al agente y recibir respuesta |
| `GET` | `/api/documents` | Listar documentos indexados |
| `POST` | `/api/documents/upload` | Subir documentos PDF o DOCX |
| `DELETE` | `/api/documents` | Eliminar documento indexado por nombre |
| `GET` | `/api/documents/{document_id}` | Descargar documento DOCX generado |

---

## Funcionalidades implementadas

1. **Agente inteligente con planificación autónoma**: El sistema analiza cada consulta del usuario y genera un plan de ejecución estructurado, seleccionando las herramientas necesarias (`rag`, `web`, `document`) en el orden lógico adecuado.

2. **Sistema RAG (Retrieval-Augmented Generation)**:
   - Carga de documentos en formatos PDF y DOCX.
   - División automática en fragmentos de 800 tokens con solapamiento de 100 tokens.
   - Indexación en base de datos vectorial ChromaDB con persistencia local.
   - Estrategia de recuperación MMR (Maximum Marginal Relevance) con parámetros configurables.
   - Listado y eliminación individual de documentos indexados.

3. **Búsqueda web en tiempo real**: Integración con la API de Tavily para obtener información actualizada de internet, con profundidad de búsqueda avanzada y límite de resultados configurable.

4. **Generación de documentos DOCX**: El agente puede generar documentos estructurados (título, objetivo, secciones y párrafos) a partir del contexto combinado de fuentes internas y externas, exportándolos como archivos `.docx` descargables.

5. **Múltiples modelos de lenguaje**: Cuatro opciones de LLM seleccionables por el usuario (Llama 4 Maverick, Gemini 2.5 Flash Lite, Qwen 3.5 Flash, DeepSeek V4), todos a través de OpenRouter.

6. **API REST documentada**: Todos los servicios expuestos mediante FastAPI con documentación Swagger autogenerada.

7. **Fusión inteligente de contextos**: El sintetizador combina resultados de RAG y búsqueda web en una respuesta unificada, coherente y estructurada.

8. **Soporte CORS**: Configuración de orígenes cruzados para integración con el frontend.

---

## Autor

**Juan Correa**  
Correo electrónico: juandev201305@gmail.com  
GitHub: [juandev201305](https://github.com/juandev201305)  
Repositorio: [agent-langchain-rag](https://github.com/juandev201305/agent-langchain-rag)