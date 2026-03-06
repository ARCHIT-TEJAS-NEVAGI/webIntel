from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_text(text):

    if not text:
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_text(text)

    # remove empty chunks
    chunks = [c.strip() for c in chunks if c.strip()]

    return chunks