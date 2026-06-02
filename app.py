from utils.doc_splitter import split_docs
from utils.embeddings import get_embeddings_model
from utils.vectorstore import create_vectorstore
from utils.qa_chain import get_llm, create_qa_chain
from utils.pdf_loader import load_pdf
from dotenv import load_dotenv

import os
import streamlit as st

load_dotenv(dotenv_path=".env")

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("OPENAI_API_KEY not found in .env file")
    st.stop()

os.environ["OPENAI_API_KEY"] = api_key
print("API KEY loaded successfully")

# Initialize models with API key
embeddings_model = get_embeddings_model(api_key)
llm = get_llm(api_key)

st.title("AskMyDoc - Posez vos questions sur votre PDF")

uploaded_file = st.file_uploader("Téléversez un PDF", type="pdf")

if "question" not in st.session_state:
    st.session_state.question = ""
    
if "history" not in st.session_state:
    st.session_state.history = []

if uploaded_file and  "qa" not in st.session_state:
    docs= load_pdf(uploaded_file)
    chunks = split_docs(docs)
    vectordb = create_vectorstore(chunks, embeddings_model)
    st.session_state.qa = create_qa_chain(vectordb, llm)

def ask_question():
    question = st.session_state.question

    if question and "qa" in st.session_state:
        result = st.session_state.qa({"query": question})


        st.session_state.history.append({
            "role": "user",
            "content": question
        })

        st.session_state.history.append({
            "role": "assistant",
            "content": result['result'],
            "sources": result['source_documents']
        })

        st.session_state.question = ""  #  reset SANS erreur


# affichage des messages d'abord
for message in st.session_state.history:
    if message["role"] == "user":
        st.markdown(f"**🧑 Toi :** {message['content']}")
    else:
        st.markdown(f"**🤖 askmydoc :** {message['content']}")
        
        if "sources" in message:
            with st.expander("📄 Sources"):
                for i, doc in enumerate(message["sources"]):
                    page = doc.metadata.get("page", "N/A")
                    clean = doc.page_content.replace("\n", " ").strip()

                    st.markdown(f"**Source {i+1}:**")
                    st.write(f"> {clean[:400]}...")
                    st.markdown(f"*Page: {page + 1}*")
#
st.text_input(
    "Posez votre question :",
    key= "question",
    on_change= ask_question
)