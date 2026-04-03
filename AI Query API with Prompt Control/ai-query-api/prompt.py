# prompt.py

def create_prompt(context: str, question: str) -> str:
    """
    Creates a prompt for the LLM with a strict system message and the retrieved context.
    """
    system_prompt = """
    Answer ONLY from the given context.
    - Do not hallucinate or make up information.
    - If the answer is not found in the context, say "I don't know".
    - Keep the answer clear and short.
    """
    
    user_prompt = f"""
    Context:
    {context}
    
    Question:
    {question}
    """
    
    return f"{system_prompt}\n{user_prompt}"
