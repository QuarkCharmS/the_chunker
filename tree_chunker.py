import os
from typing import List
from tree_sitter_languages import get_parser  # <-- correct import for tree_sitter_languages
from chunker_config import LANG_FUNCTION_NODES, EXT_TO_LANG, CHUNKABLE_LANGUAGES

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

def extract_code_blocks(code: str, language_name: str) -> List[str]:
    
    if language_name not in CHUNKABLE_LANGUAGES:
        print(f"Skipping tree-sitter for {language_name}, treating as plain text.")
        return [code]

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
        print(f"Checking node type: {node.type}")
        if node.type in valid_node_types:
            chunks.append(code[node.start_byte:node.end_byte])
        for child in node.children:
            chunks.extend(recurse(child))
        return chunks

    print("Parsing complete. Returning results.")
    return recurse(root)

# === Test run ===

#filepath = "/home/santiago/dummy-files-for-project-testing/dummy.c"

#with open(filepath, 'r') as f:
#    code = f.read()

#lang_type = resolve_language_from_path(filepath)

#print(f"Trying file: {filepath}")
#print(f"Detected language: {lang_type}")

#chunks = extract_code_blocks(code, lang_type)

#print(chunks)

#for i, chunk in enumerate(chunks):
#    print(f"\n--- Chunk {i+1} ---\n{chunk}")
