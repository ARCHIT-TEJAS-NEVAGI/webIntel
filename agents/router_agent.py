def route_query(query):

    if "http://" in query or "https://" in query:
        return "scrape"

    if "calculate" in query or "sum" in query:
        return "tool"

    return "rag"