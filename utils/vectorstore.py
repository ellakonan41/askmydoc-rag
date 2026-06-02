from langchain_chroma import Chroma

## code pour creer une base de donnees vectorielle à partir de documents (avec metadata)##
def create_vectorstore(chunks, embeddings):
    vectordb = Chroma.from_documents(chunks, embeddings)
    #vectordb = Chroma.from_texts(chunks, embeddings)
    return vectordb