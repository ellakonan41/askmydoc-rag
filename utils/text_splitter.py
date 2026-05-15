# # utils/text_splitter.py
from langchain_text_splitters import RecursiveCharacterTextSplitter   


## decoupage en text plutot qu'en document##
# def split_text(text):
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=500,
#         chunk_overlap=50
#     )
#     chunks = splitter.split_text(text)
#     return chunks



def split_docs(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    return splitter.split_documents(docs)