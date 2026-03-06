# Embeddings database module
from langchain_community.embeddings import OllamaEmbeddings
from config.settings import EMBEDDING_MODEL

def get_embeddings():
    return OllamaEmbeddings(
        model=EMBEDDING_MODEL
    )