import os
import tempfile
import streamlit as st

from config.models import GENERATION_MODEL

from rag.retriever import initialize_retriever
from rag.document_loader import load_document
from rag.chunker import splitter_docs
from rag.vector_store import load_vector_store, get_indexed_files, delete_document

from services.llm_factory import get_llm
from services.llm_planner import build_plan
from pipelines.unified_pipeline import execute_plan


# =========================
# CONFIGURACIÓN GENERAL
# =========================
st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.title("Agente en Desarrollo")


# =========================
# ESTADO DE SESIÓN
# =========================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# =========================
# SIDEBAR: INGESTA DOCS
# =========================
with st.sidebar:

    st.subheader("📄 Documentos")

    uploaded_files = st.file_uploader(
        "Sube tus documentos",
        type=["docx", "pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:
        st.success(
            f"{len(uploaded_files)} archivos cargados"
        )

        if st.button("Procesar documentos"):

            with st.spinner(
                "Procesando documentos..."
            ):

                vector_store = load_vector_store()

                for file in uploaded_files:

                    ext = os.path.splitext(
                        file.name
                    )[1]

                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=ext
                    ) as tmp:

                        tmp.write(file.getbuffer())
                        path = tmp.name

                    document = load_document(path)

                    docs = splitter_docs(
                        document,
                        source_path=file.name
                    )

                    vector_store.add_documents(docs)

            st.success(
                "Documentos indexados"
            )


# =========================
# MODELO
# =========================
selected_model_label = st.sidebar.selectbox(
    "Selecciona el modelo de IA",
    options=list(
        GENERATION_MODEL.keys()
    )
)

selected_model = GENERATION_MODEL[
    selected_model_label
]

st.sidebar.info(
    f"Modelo:\n{selected_model}"
)


# =========================
# CHAT
# =========================
st.header("💬 Chat")

for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.write(message)


query = st.chat_input(
    "Escribe tu mensaje..."
)

if query:

    st.session_state.chat_history.append(
        ("user", query)
    )

    with st.chat_message("user"):
        st.write(query)

    with st.spinner("Pensando..."):

        llm = get_llm(selected_model)

        retriever = initialize_retriever()

        # Construcción del plan
        plan = build_plan(
            query=query,
            llm=llm
        )

        # Debug visual planner
        with st.expander(
            "🧠 Plan del agente"
        ):
            st.json(
                plan.model_dump()
            )

        # Ejecución del plan
        state = execute_plan(
            plan=plan,
            query=query,
            retriever=retriever,
            llm_model=llm
        )

        # Contexto consolidado
        final_context = "\n\n".join(
            filter(None, [
                state["web_context"],
                state["rag_context"]
            ])
        )

        # Si no hay contexto, usar query
        if not final_context.strip():
            final_context = query

        # Respuesta final del agente
        response = llm.invoke(
            f"""
            Responde al usuario de forma clara
            usando este contexto:

            {final_context}

            Pregunta:
            {query}
            """
        )

        response_text = response.content

    st.session_state.chat_history.append(
        ("assistant", response_text)
    )

    with st.chat_message("assistant"):

        st.write(response_text)

        # Descargar DOCX si fue generado
        if state["document_path"]:
            st.download_button(
                label="⬇ Descargar DOCX",
                data=state["document_path"],
                file_name="documento.docx",
                mime=(
                    "application/vnd.openxmlformats-"
                    "officedocument.wordprocessingml.document"
                )
            )


# =========================
# DOCUMENTOS INDEXADOS
# =========================
st.sidebar.subheader(
    "📂 Documentos indexados"
)

vector_store = load_vector_store()

files = get_indexed_files(
    vector_store
)

for file in files:

    col1, col2 = st.sidebar.columns(
        [3, 1]
    )

    col1.write(file)

    if col2.button(
        "❌",
        key=file
    ):
        delete_document(
            vector_store,
            file
        )

        st.rerun()