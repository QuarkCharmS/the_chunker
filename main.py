import os
from chunking import chunk_file  # <- this now uses dispatcher logic
from typing import List, Dict

INPUT_FILE = "/home/santiago/dummy-files-for-project-testing/Dockerfile"

def main():
    # 1. Use dispatcher to get chunks (tree-sitter or chonkie fallback)
    blocks = chunk_file(INPUT_FILE)

    if not blocks:
        print(f"[WARN] No blocks found in {INPUT_FILE}")
        return

    
    #print(blocks)
    # 2. Tokenize chunks
    #tokenized_blocks = assign_tokens_to_blocks(blocks)

    # 3. Output results
    for i, block in enumerate(blocks, start=1):
        print(f"--- Block {i} ---")
        print(f"Tokens: {block['tokens']}")
        print(block['content'])
        print("-" * 50)

if __name__ == "__main__":
    main()

