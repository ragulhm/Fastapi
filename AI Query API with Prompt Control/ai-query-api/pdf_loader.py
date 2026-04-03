# pdf_loader.py

import os
import fitz  # PyMuPDF
from config import BOOKS_DIR

def load_pdfs():
    """
    Loads all PDF files from the 'books' directory and extracts text.
    """
    pdf_texts = {}
    if not os.path.exists(BOOKS_DIR):
        raise FileNotFoundError(f"The directory '{BOOKS_DIR}' was not found.")

    pdf_files = [f for f in os.listdir(BOOKS_DIR) if f.endswith(".pdf")]
    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in the '{BOOKS_DIR}' directory.")

    for pdf_file in pdf_files:
        file_path = os.path.join(BOOKS_DIR, pdf_file)
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            pdf_texts[pdf_file] = text
        except Exception as e:
            print(f"Error processing {pdf_file}: {e}")
    
    return pdf_texts

def split_text_into_chunks(text: str, chunk_size: int):
    """
    Splits a long text into smaller chunks of a specified size.
    """
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield ' '.join(words[i:i + chunk_size])

