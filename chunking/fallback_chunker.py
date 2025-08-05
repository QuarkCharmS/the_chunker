from chonkie import RecursiveChunker
from typing import List
from .tokenizer import count_tokens

MAX_CHUNKING_SIZE = 350 # This number was chosen because for a model like qwen it guarantees enough wiggle space when later wanting to create the RAG chunking 

_chunker = RecursiveChunker(chunk_size=MAX_CHUNKING_SIZE)

def fallback_chunk(file_text: str) -> List[str]: 
    print("File not identified as code, using Fallback strategy")

    chunks = _chunker(file_text)

    return [{"content": c.text.strip(), "tokens": count_tokens(c.text.strip())} for c in chunks if c.text.strip()]
