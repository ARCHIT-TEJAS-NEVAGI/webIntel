from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

from agents.crawler_agent import crawl_website
from agents.rag_agent import ask_question
from utils.text_chunker import chunk_text
from database.vector_store import get_vector_store


# -----------------------------
# Logging Setup
# -----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# -----------------------------
# FastAPI Initialization
# -----------------------------
app = FastAPI(
    title="WebIntel AI",
    description="AI-powered website intelligence and research assistant",
    version="1.0"
)


# -----------------------------
# CORS Configuration
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change later to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Initialize Vector Store
# -----------------------------
vector_store = get_vector_store()


# -----------------------------
# Request Models
# -----------------------------
class ScrapeRequest(BaseModel):
    url: str


class AskRequest(BaseModel):
    question: str


# -----------------------------
# Root Endpoint
# -----------------------------
@app.get("/")
async def root():
    return {
        "message": "WebIntel AI backend running",
        "status": "healthy"
    }


# -----------------------------
# Scrape Website Endpoint
# -----------------------------
@app.post("/scrape")
async def scrape_website(request: ScrapeRequest):

    try:

        logger.info(f"Starting crawl for: {request.url}")

        pages = crawl_website(request.url)

        if not pages:
            raise HTTPException(
                status_code=400,
                detail="Website scraping returned no data"
            )

        total_chunks = 0

        for page in pages:

            chunks = chunk_text(page)

            if chunks:
                vector_store.add_texts(
                    texts=chunks,
                    metadatas=[{"source": request.url}] * len(chunks)
                )

                total_chunks += len(chunks)

        logger.info(f"Stored {total_chunks} chunks from {len(pages)} pages")

        return {
            "status": "success",
            "pages_scraped": len(pages),
            "chunks_stored": total_chunks
        }

    except Exception as e:

        logger.error(f"Scraping failed: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# -----------------------------
# Ask AI Endpoint
# -----------------------------
@app.post("/ask")
async def ask_ai(request: AskRequest):

    try:

        logger.info(f"User question: {request.question}")

        answer = ask_question(request.question)

        return {
            "question": request.question,
            "answer": answer
        }

    except Exception as e:

        logger.error(f"AI query failed: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )