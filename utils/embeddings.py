from langchain_openai import OpenAIEmbeddings

def get_embeddings_model(api_key):
    return OpenAIEmbeddings(api_key=api_key)
