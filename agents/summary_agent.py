from langchain_community.chat_models import ChatOllama
from database.vector_store import get_vector_store
from config.settings import OLLAMA_MODEL

def summarize_website():

    vector_store = get_vector_store()

    docs = vector_store.similarity_search("website overview", k=5)

    context = "\n".join([doc.page_content for doc in docs])

    llm = ChatOllama(model=OLLAMA_MODEL)

    prompt = f"""
Summarize the following website content:

{context}

Provide a clear overview of the website.
"""

    response = llm.invoke(prompt)

    return response.content