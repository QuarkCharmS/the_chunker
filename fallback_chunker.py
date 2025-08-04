from chonkie import RecursiveChunker
from typing import List

_chunker = RecursiveChunker()

def fallback_chunk_from_file(file_text: str) -> List[str]:

    chunks = _chunker(file_text)
    return [c.text.strip() for c in chunks if c.text.strip()]

file_path = "/home/santiago/dummy-files-for-project-testing/dummy.json"

with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

chunk_list = fallback_chunk_from_file(text)

for i, chunk in enumerate(chunk_list, start=1):
    print(f"--- Chunk {i} ---")
    print(chunk)
    print()
