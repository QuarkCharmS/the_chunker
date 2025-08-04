from chonkie import RecursiveChunker
from typing import List

_chunker = RecursiveChunker()

def fallback_chunk_from_file(file_text: str) -> List[str]: 
    print("File not identified as code, using Fallback strategy")

    chunks = _chunker(file_text)
    return [c.text.strip() for c in chunks if c.text.strip()]
