from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


def get_vector_store():

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    vector_store = Chroma(
        collection_name="webintel",
        embedding_function=embeddings,
        persist_directory="./chroma_db"
    )

    return vector_store