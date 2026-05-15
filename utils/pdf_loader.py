
## version pour charger et extraire en document (avec metadata)##
import tempfile
from langchain_community.document_loaders import PyPDFLoader

def load_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    loader = PyPDFLoader(tmp_path)
    return loader.load()


## version pour pouvoir charger et extraire en text##
# from pypdf import PdfReader

# def load_pdf(file_path):
#     """
#     Load a PDF file and extract its text content.

#     Args:
#         file_path (str): The path to the PDF file.
#     Returns:
#         str: The extracted text content from the PDF.       

#     """
#     reader= PdfReader(file_path)
#     text=""
#     for page in reader.pages:
#         text+=page.extract_text() + "\n"
#     return text