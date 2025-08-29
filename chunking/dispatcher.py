# dispatcher.py
import os
from .chunker_config import get_language_from_extension, is_chunkable
from .tree_chunker import extract_code_blocks
from .fallback_chunker import fallback_chunk
from .read_file_content import read_file_content 


def chunk_file(file_path: str, model_name: str) -> list[dict]:
    """
    Main entry point for chunking files.
    Returns list of dictionaries with 'content' and 'tokens' keys.
    """
    # Use the centralized language resolution from config
    language = get_language_from_extension(file_path)
    print(f"[INFO] Identified language: {language} for file: {os.path.basename(file_path)}")
    
    try:
        content = read_file_content(file_path)
        
        if content == "":
            print("[INFO] File is empty")
            return []

    except Exception as e:
        print(f"[ERROR] Could not read file {file_path}: {e}")
        return []
    
    if is_chunkable(language):
        print(f"[INFO] Using tree-sitter chunking for {language}")
        try:
            code_blocks = extract_code_blocks(content, language, model_name)
            if code_blocks == []:
                print("[INFO] No code blocks were extracted from file, using fallback strategy instead")
                return fallback_chunk(content, model_name)
            return code_blocks
        except Exception as e:
            print(f"[WARNING] Tree-sitter chunking failed for {language}: {e}")
            print(f"[INFO] Falling back to basic chunking")
            return fallback_chunk(content, model_name)
    else:
        print(f"[INFO] Using fallback chunking for {language}")
        return fallback_chunk(content, model_name)
