from langchain_classic.chains import RetrievalQA
from langchain_openai import ChatOpenAI   

def get_llm(api_key, temperature=0):
    return ChatOpenAI(api_key=api_key, temperature=temperature)

def create_qa_chain(vectordb, llm):
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectordb.as_retriever(search_kwargs={"k": 3},search_type="similarity"),
        return_source_documents=True
    )
    return qa