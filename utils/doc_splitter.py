
from langchain_text_splitters import RecursiveCharacterTextSplitter   

## decoupage en document plutot qu'en text##
def split_docs(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    return splitter.split_documents(docs)



