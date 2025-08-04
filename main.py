import os
from tree_chunker import extract_code_blocks, resolve_language_from_path
from tokenizer import count_tokens
from typing import List, Dict

# --- File to process ---
INPUT_FILE = "/home/santiago/dummy-files-for-project-testing/dummy.xml"  # Replace with your actual path

def assign_tokens_to_blocks(blocks: List[str]) -> List[Dict]:
    """
    Given a list of code blocks, return a list of dicts:
    { content: block_text, tokens: number of tokens }
    """
    return [
        {
            "content": block,
            "tokens": count_tokens(block)
        }
        for block in blocks
    ]

def main():
    # 1. Load file
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        code = f.read()

    # 2. Detect programming language
    language = resolve_language_from_path(INPUT_FILE)

    # 3. Extract logical code blocks (functions, classes, etc.)
    blocks = extract_code_blocks(code, language)

    if not blocks:
        print(f"[WARN] No blocks found in {INPUT_FILE}")
        return

    # 4. Tokenize each block using Qwen3 tokenizer
    tokenized_blocks = assign_tokens_to_blocks(blocks)
    print(tokenized_blocks)

    # 5. Output result
    for i, item in enumerate(tokenized_blocks):
        print(f"--- Block {i + 1} ---")
        print(f"Tokens: {item['tokens']}")
        print(item['content'])
        print("-" * 50)

if __name__ == "__main__":
    main()

