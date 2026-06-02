
## Code pour charger et extraire en document (Texte +metadata)##
import tempfile
from langchain_community.document_loaders import PyPDFLoader

def load_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    loader = PyPDFLoader(tmp_path)
    return loader.load()

