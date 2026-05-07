Un chatbot local con **Retrieval-Augmented Generation (RAG)** que permite subir documentos PDF o Word y hacerles preguntas en lenguaje natural. Construido con LangChain, ChromaDB y Streamlit.

---

## ¿Qué hace?

- Sube uno o más archivos `.pdf` o `.docx`
- El sistema los divide en fragmentos y los indexa en una base vectorial (ChromaDB)
- Luego puedes chatear con el contenido usando el modelo de lenguaje que elijas
- Los documentos persisten entre sesiones y puedes eliminarlos individualmente

---

## Stack

| Capa | Tecnología |
|---|---|
| UI | Streamlit |
| Embeddings | `qwen/qwen3-embedding-8b` vía OpenRouter |
| Vector Store | ChromaDB (local) |
| LLM | Llama 4, Gemini Flash, Qwen, Deepseek (seleccionable) |
| Orquestación | LangChain |

---

## Instalación

```bash
git clone https://github.com/juandev201305/agent-langchain-rag.git
cd rag-chatbot
pip install -r requirements.txt
```

Crea un archivo `.env` en la raíz:

```env
OPENAI_API_KEY=tu_api_key_de_openrouter
```

> El proyecto usa [OpenRouter](https://openrouter.ai/) como proveedor de la API, compatible con el cliente de OpenAI.

---

## Uso

```bash
streamlit run app.py
```

1. Sube un PDF o Word desde el sidebar
2. Haz clic en **"Procesar documentos"**
3. Selecciona el modelo de generación
4. ¡Empieza a chatear!

---

## Estructura

```
├── app.py            # Interfaz Streamlit
├── pipeline.py       # Cadena RAG (retriever → LLM → respuesta)
├── rag_system.py     # Inicialización del retriever
├── vector_store.py   # Carga, split e indexado de documentos
├── prompts.py        # Prompt del sistema
├── config.py         # Modelos y parámetros
└── chroma_db/        # Base vectorial local (generada automáticamente)
```

---

## Configuración

Los parámetros del retriever y los modelos disponibles se configuran en `config.py`:

```python
SEARCH_TYPE = "mmr"         # Máxima Relevancia Marginal
SEARCH_K = 6                # Chunks recuperados por consulta
MMR_DIVERSITY_LAMBDA = 0.7  # Balance relevancia/diversidad
```

---

## Notas

- La base vectorial se guarda en `./chroma_db/` y persiste entre ejecuciones
- Puedes eliminar documentos individuales desde el sidebar sin resetear toda la base
- El sistema usa MMR como estrategia de búsqueda para evitar recuperar chunks redundantes
