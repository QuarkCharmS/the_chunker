from chonkie import RecursiveChunker
from typing import List
from .tokenizer import count_tokens

MAX_CHUNKING_SIZE = 400  # Target token size per chunk

_chunker = RecursiveChunker(chunk_size=MAX_CHUNKING_SIZE)

def fallback_chunk(file_text: str, model_name: str) -> List[dict]:
    chunks = _chunker(file_text)
    
    result = []
    for c in chunks:
        text = c.text  # preserve as-is: no strip, no whitespace removal

        if text.strip():  # only skip completely empty chunks (e.g. whitespace-only)
            result.append({
                "content": text,              # exact content with indentation
                "tokens": count_tokens(text, model_name)  # count tokens on real, unmodified text
            })

    return result
