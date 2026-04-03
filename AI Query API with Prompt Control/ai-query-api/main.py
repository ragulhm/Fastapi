# main.py

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from models import QueryRequest, QueryResponse
from rag import get_rag_response
from pdf_loader import load_pdfs, split_text_into_chunks
from vector_db import vector_db
from config import CHUNK_SIZE

app = FastAPI(
    title="AI Query API with Prompt Control",
    description="A production-style FastAPI project for querying PDFs using RAG.",
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def startup_event():
    """
    On startup, load PDFs, split them into chunks, and add them to the vector DB.
    """
    try:
        print("Loading and processing PDFs...")
        pdf_texts = load_pdfs()
        all_chunks = []
        for pdf_name, text in pdf_texts.items():
            chunks = list(split_text_into_chunks(text, CHUNK_SIZE))
            all_chunks.extend(chunks)
        
        if all_chunks:
            vector_db.add_documents(all_chunks)
            print(f"Added {len(all_chunks)} chunks to the vector database.")
        else:
            print("No text chunks to add to the database.")
            
    except FileNotFoundError as e:
        print(f"Error during startup: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during startup: {e}")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Serves the main HTML page.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/query", response_model=QueryResponse)
def query_endpoint(request: QueryRequest):
    """
    Endpoint to receive a question and return a RAG-based answer.
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    try:
        response = get_rag_response(request.question)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
