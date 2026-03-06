from langchain_google_genai import ChatGoogleGenerativeAI
from database.vector_store import get_vector_store


def ask_question(question):

    vector_store = get_vector_store()

    retriever = vector_store.as_retriever(
        search_kwargs={"k":5}
    )

    docs = retriever.invoke(question)

    context = "\n\n".join([d.page_content for d in docs])

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.2
    )

    prompt = f"""
Answer the question based on the following context.

Context:
{context}

Question:
{question}
"""

    response = llm.invoke(prompt)

    return response.content