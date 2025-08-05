import os
from chunking import chunk_file  # <- this now uses dispatcher logic
from overlap_chunker import process_file_with_overlap
from typing import List, Dict

INPUT_FILE = "/home/santiago/dummy-files-for-project-testing/Dockerfile"

def main():
    # 1. Use dispatcher to get semantic chunks (tree-sitter or fallback)
    semantic_chunks = chunk_file(INPUT_FILE)
    
    if not semantic_chunks:
        print(f"[WARN] No blocks found in {INPUT_FILE}")
        return
    
    print(f"\n[INFO] Got {len(semantic_chunks)} semantic chunks from {os.path.basename(INPUT_FILE)}")
    
    # 2. Create overlapping chunks for embedding model
    # Using default settings: 400 token target, 100 token overlap
    final_chunks = process_file_with_overlap(
        semantic_chunks,
        method="overlap",  # or "sliding_window"
        target_size=400,
        overlap_tokens=100,
        max_chunk_size=512  # Qwen-3 can handle up to 512 tokens typically
    )
    
    print(f"[INFO] Created {len(final_chunks)} overlapping chunks for embedding")
    
    # 3. Output results
    print("\n" + "="*60)
    print("SEMANTIC CHUNKS (from tree-sitter/fallback):")
    print("="*60)
    
    for i, block in enumerate(semantic_chunks[:3], start=1):  # Show first 3
        print(f"\n--- Semantic Chunk {i} ---")
        print(f"Tokens: {block['tokens']}")
        print(block['content'][:200] + "..." if len(block['content']) > 200 else block['content'])
    
    if len(semantic_chunks) > 3:
        print(f"\n... and {len(semantic_chunks) - 3} more semantic chunks")
    
    print("\n" + "="*60)
    print("FINAL OVERLAPPING CHUNKS (for Qwen-3 embedding):")
    print("="*60)
    
    for i, chunk in enumerate(final_chunks, start=1):
        print(f"\n--- Final Chunk {i} ---")
        print(f"Tokens: {chunk['tokens']}")
        print(f"Metadata: {chunk['metadata']}")
        print(f"Content:\n{chunk['content']}")
        print("-" * 50)
    
    # 4. Summary statistics
    print("\n" + "="*60)
    print("SUMMARY:")
    print("="*60)
    print(f"Original semantic chunks: {len(semantic_chunks)}")
    print(f"Total tokens in semantic chunks: {sum(c['tokens'] for c in semantic_chunks)}")
    print(f"Final overlapping chunks: {len(final_chunks)}")
    print(f"Average tokens per final chunk: {sum(c['tokens'] for c in final_chunks) / len(final_chunks):.1f}")
    
    # Check if chunks are within expected size
    oversized = [c for c in final_chunks if c['tokens'] > 512]
    if oversized:
        print(f"\n[WARN] {len(oversized)} chunks exceed 512 tokens!")
    else:
        print(f"\n[SUCCESS] All chunks are within 512 token limit for Qwen-3")

if __name__ == "__main__":
    main()
