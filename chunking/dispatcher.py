import os
from .chunker_config import EXT_TO_LANG, CHUNKABLE_LANGUAGES
from .tree_chunker import extract_code_blocks
from .fallback_chunker import fallback_chunk

def resolve_language_from_path(path: str) -> str:
    basename = os.path.basename(path)
    ext = os.path.splitext(basename)[1]

    if basename == "Dockerfile":
        return "dockerfile"
    if basename == "Jenkinsfile":
        return "groovy"
    if basename == "Makefile":
        return "make"
    if basename == "CMakeLists.txt":
        return "cmake"

    return EXT_TO_LANG.get(ext.lower(), "default")

def chunk_file(file_path: str) -> list[str]:
    language = resolve_language_from_path(file_path)
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError as e:
        print(f"[ERROR] Could not read file {file_path}: {e}")
        return []
    
    if language in CHUNKABLE_LANGUAGES:
        return extract_code_blocks(content, language)

    return fallback_chunk(content)

