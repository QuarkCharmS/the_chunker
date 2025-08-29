from transformers import AutoTokenizer
from typing import List, Dict

# This is the exact model you're using for embedding.
# Qwen3 has a specific tokenizer – don't fuck around with tiktoken or GPT tokenizers here.

# Load the tokenizer from HuggingFace.
# `trust_remote_code=True` is REQUIRED because Qwen uses a custom tokenizer class (QwenTokenizer).

def count_tokens(text: str, model_name: str) -> int:
    """
    Count the number of tokens in a single string using the Qwen3 tokenizer.
    No special tokens like [CLS] or [SEP] are added—this is raw count.
    """
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    except RepositoryNotFoundError:
        print(f"Model '{model_name}' not found")
        raise
    except ConnectionError:
        print("Network connection failed")
        raise
    except OSError as e:
        if "401" in str(e):
            print("Authentication required - need HF token")
        elif "403" in str(e):
            print("Access forbidden - private model")
        else:
            print(f"File/permission error: {e}")
        raise
    except ValueError as e:
        print(f"Invalid tokenizer config: {e}")
        raise
    except ImportError as e:
        print(f"Missing dependency: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

    return len(tokenizer.encode(text, add_special_tokens=False))

def assign_tokens_to_blocks(blocks: List[str], model_name:  str) -> List[Dict]:
    """
    Take a list of text blocks (e.g., code chunks) and return a list of dictionaries,
    where each dict contains the original text and its token count.

    Useful for deciding how to chunk content later based on token limits.
    """
    return [
        {
            "text": block,               # Original code/text block
            "tokens": count_tokens(block, model_name)  # How many tokens Qwen3 sees in this block
        }
        for block in blocks
    ]

