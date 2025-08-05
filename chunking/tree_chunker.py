from typing import List
from tree_sitter_languages import get_parser  # <-- correct import for tree_sitter_languages
from .chunker_config import LANG_FUNCTION_NODES
from .tokenizer import count_tokens 
from .fallback_chunker import fallback_chunk

def extract_code_blocks(code: str, language_name: str) -> List[str]:  

    try:
        parser = get_parser(language_name)
        if parser is None:
            print(f"[ERROR] No parser found for language: {language_name}")
            return []
    except Exception as e:
        print(f"[ERROR] Failed to load parser for '{language_name}': {e}")
        return []

    print("Starting the parsing process...")

    tree = parser.parse(bytes(code, "utf8"))
    root = tree.root_node

    valid_node_types = LANG_FUNCTION_NODES.get(language_name, LANG_FUNCTION_NODES["default"])

    print(f"Valid node types for '{language_name}': {valid_node_types}")

    def recurse(node):
        chunks = []
        if node.type in valid_node_types:
            chunk_content = code[node.start_byte:node.end_byte]
            tokens = count_tokens(chunk_content)
            
            if tokens > 400:
                content_to_append = fallback_chunk(chunk_content)
                chunks.extend(content_to_append)
            else: 
                chunks.append({
                    "content": chunk_content,
                    "tokens": tokens
                    })
        for child in node.children:
            chunks.extend(recurse(child))
        return chunks

    print("Parsing complete. Returning results.")
    return recurse(root)
