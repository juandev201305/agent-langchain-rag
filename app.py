import streamlit as st
import os
import tempfile
from config import GENERATION_MODEL
from vector_store import (
    splitter_docs, load_vector_store, load_document,
    get_indexed_files, delete_document
)
from rag_system import initialize_retriever
from pipeline import rag_chain, generator_chain, web_search_chain


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
# SIDEBAR: ELECCIÓN MODO
# =========================
mode = st.sidebar.radio(
    "Modo",
    ["Chat", "Generator_docx"]
)


# =========================
# SIDEBAR: INGESTA DOCX
# =========================
with st.sidebar:
    uploaded_files = st.file_uploader(
        "Sube tus documentos",
        type=["docx", "pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:
        st.success(f"{len(uploaded_files)} archivos cargados")

        if st.button("Procesar documentos"):
            with st.spinner("Procesando documentos..."):
                vector_store = load_vector_store()

                for file in uploaded_files:
                    ext = os.path.splitext(file.name)[1]

                    # Guardar temporalmente en disco
                    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
                        tmp.write(file.getbuffer())
                        path = tmp.name

                    document = load_document(path)
                    docs = splitter_docs(document, source_path=file.name)
                    vector_store.add_documents(docs)

            st.success("Documentos indexados en Chroma")


# Selector de modelo
selected_model_label = st.sidebar.selectbox(
    "Selecciona el modelo de IA",
    options=list(GENERATION_MODEL.keys())
)
selected_model = GENERATION_MODEL[selected_model_label]
st.sidebar.info(f"Modelo seleccionado:\n{selected_model}")


# =========================
# GENERADOR DOCX
# =========================
if mode == "Generator_docx":
    st.header("📄 Generador DOCX")

    prompt_doc = st.text_area(
        "Describe el documento que quieres generar",
        height=200,
        placeholder=(
            "Ejemplo:\n"
            "Haz un informe técnico sobre IA generativa,\n"
            "con introducción, desarrollo, ventajas,\n"
            "desventajas y conclusión."
        )
    )

    if st.button("Generar documento"):
        if not prompt_doc.strip():
            st.warning("Debes escribir un prompt")
        else:
            with st.spinner("Generando documento..."):
                docx_file = generator_chain(prompt_doc, selected_model)

            st.success("Documento generado")
            st.download_button(
                label="⬇ Descargar DOCX",
                data=docx_file,
                file_name="documento.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )


# =========================
# MAIN: CHAT
# =========================
if mode == "Chat":
    st.header("💬 Chat")

    # Toggle de búsqueda web — vive arriba del chat, no como modo separado
    use_web = st.toggle(
        "🌐 Buscar en internet",
        value=False,
        help=(
            "Activado: la respuesta se genera buscando en la web.\n"
            "Desactivado: se consulta solo tus documentos indexados."
        )
    )

    # Etiqueta de contexto activo
    if use_web:
        st.caption("Modo activo: **búsqueda web**")
    else:
        st.caption("Modo activo: **documentos indexados**")

    # Historial del chat
    for role, message in st.session_state.chat_history:
        with st.chat_message(role):
            st.write(message)

    # Input del usuario
    query = st.chat_input("Escribe tu pregunta...")

    if query:
        st.session_state.chat_history.append(("user", query))
        with st.chat_message("user"):
            st.write(query)

        with st.spinner("Pensando..."):
            if use_web:
                # Busca en internet con web_search_chain
                response = web_search_chain(query, selected_model)
            else:
                # RAG sobre documentos indexados
                retriever = initialize_retriever()
                response = rag_chain(query, retriever, selected_model)

        st.session_state.chat_history.append(("assistant", response))
        with st.chat_message("assistant"):
            st.write(response)


# =========================
# SIDEBAR: DOCUMENTOS INDEXADOS
# =========================
st.sidebar.subheader("📂 Documentos indexados")

vector_store = load_vector_store()
files = get_indexed_files(vector_store)

for file in files:
    col1, col2 = st.sidebar.columns([3, 1])
    col1.write(file)

    if col2.button("❌", key=file):
        delete_document(vector_store, file)
        st.rerun()