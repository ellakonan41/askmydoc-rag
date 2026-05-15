from langchain_chroma import Chroma

## version pour creer un vectorstore a partir de documents (avec metadata)##
def create_vectorstore(chunks, embeddings):
    vectordb = Chroma.from_documents(chunks, embeddings)
    #vectordb = Chroma.from_texts(chunks, embeddings)
    return vectordb