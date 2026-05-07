import streamlit as st
import os
import tempfile
from config import GENERATION_MODEL
from vector_store import splitter_docs, build_vector_store, load_vector_store, reset_chroma, load_document, get_indexed_files, delete_document
from rag_system import initialize_retriever
from pipeline import rag_chain


# =========================
# CONFIGURACIÓN GENERAL
# =========================
st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="",
    layout="wide"
)

st.title("Agente en Desarrollo")

# =========================
# ESTADO DE SESIÓN
# =========================
if "vector_ready" not in st.session_state:
    st.session_state.vector_ready = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# =========================
# SIDEBAR: INGESTA DOCX
# =========================

file_paths = []

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
                    
                    # 1. Guardar temporalmente
                    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
                        tmp.write(file.getbuffer())
                        path = tmp.name

                    # 2. Cargar documento antes de ser procesado 
                    document = load_document(path)

                    # 3. Split
                    docs = splitter_docs(document, source_path=file.name)

                    # 4. Indexar
                    vector_store.add_documents(docs)

            st.success("Documentos indexados en Chroma")



selected_model_label = st.sidebar.selectbox(
    "Selecciona el modelo de IA",
    options=list(GENERATION_MODEL.keys())
)

selected_model = GENERATION_MODEL[selected_model_label]

st.sidebar.info(f"Modelo seleccionado:\n{selected_model}")

# =========================
# MAIN: CHAT
# =========================
st.header("💬 Chat")

# Mostrar historial
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.write(message)


# Input del usuario
query = st.chat_input("Haz una pregunta sobre el documento...")

if query:
    # Mostrar pregunta
    st.session_state.chat_history.append(("user", query))
    with st.chat_message("user"):
        st.write(query)

    # Obtener respuesta
    with st.spinner("Pensando..."):
        retriever = initialize_retriever()
        response = rag_chain(query, retriever, selected_model)

    # Mostrar respuesta
    st.session_state.chat_history.append(("assistant", response))
    with st.chat_message("assistant"):
        st.write(response)


# =========================
# EXTRA: RESET
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