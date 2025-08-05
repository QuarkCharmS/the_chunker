from transformers import AutoTokenizer
from typing import List, Dict

# This is the exact model you're using for embedding.
# Qwen3 has a specific tokenizer – don't fuck around with tiktoken or GPT tokenizers here.
MODEL_NAME = "Qwen/Qwen3-Embedding-8B"

# Load the tokenizer from HuggingFace.
# `trust_remote_code=True` is REQUIRED because Qwen uses a custom tokenizer class (QwenTokenizer).
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)

def count_tokens(text: str) -> int:
    """
    Count the number of tokens in a single string using the Qwen3 tokenizer.
    No special tokens like [CLS] or [SEP] are added—this is raw count.
    """
    return len(tokenizer.encode(text, add_special_tokens=False))

def assign_tokens_to_blocks(blocks: List[str]) -> List[Dict]:
    """
    Take a list of text blocks (e.g., code chunks) and return a list of dictionaries,
    where each dict contains the original text and its token count.

    Useful for deciding how to chunk content later based on token limits.
    """
    return [
        {
            "text": block,               # Original code/text block
            "tokens": count_tokens(block)  # How many tokens Qwen3 sees in this block
        }
        for block in blocks
    ]

