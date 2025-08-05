# dispatcher.py
import os
from .chunker_config import get_language_from_extension, is_chunkable
from .tree_chunker import extract_code_blocks
from .fallback_chunker import fallback_chunk

def chunk_file(file_path: str) -> list[dict]:
    """
    Main entry point for chunking files.
    Returns list of dictionaries with 'content' and 'tokens' keys.
    """
    # Use the centralized language resolution from config
    language = get_language_from_extension(file_path)
    print(f"[INFO] Identified language: {language} for file: {os.path.basename(file_path)}")
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError as e:
        print(f"[ERROR] Could not read file {file_path}: {e}")
        return []
    
    if is_chunkable(language):
        print(f"[INFO] Using tree-sitter chunking for {language}")
        try:
            return extract_code_blocks(content, language)
        except Exception as e:
            print(f"[WARNING] Tree-sitter chunking failed for {language}: {e}")
            print(f"[INFO] Falling back to basic chunking")
            return fallback_chunk(content)
    else:
        print(f"[INFO] Using fallback chunking for {language}")
        return fallback_chunk(content)
