# rag.py

from vector_db import vector_db
from llm import get_llm_response
from prompt import create_prompt
from config import TOP_K
from logger import log_event

def get_rag_response(question: str):
    """
    Retrieves relevant context, generates a prompt, gets the LLM response, and logs the event.
    """
    # 1. Retrieve relevant context from the vector DB
    retrieved_context = vector_db.query(query_text=question, n_results=TOP_K)
    
    if not retrieved_context:
        return {
            "answer": "I don't know.",
            "source": "No relevant context found.",
            "confidence": "low"
        }
        
    context_str = "\n\n".join(retrieved_context)

    # 2. Create a prompt for the LLM
    prompt = create_prompt(context=context_str, question=question)

    # 3. Get the response from the LLM
    try:
        answer = get_llm_response(prompt)
    except Exception as e:
        return {
            "answer": f"Error from LLM: {e}",
            "source": "API Failure",
            "confidence": "low"
        }

    # 4. Log the event
    log_event(question=question, context=context_str, answer=answer)

    # 5. Determine confidence
    confidence = "high" if "I don't know" not in answer else "low"

    return {
        "answer": answer,
        "source": "From retrieved context",
        "confidence": confidence
    }
