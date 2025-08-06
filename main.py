import os
from chunking import chunk_file  # <- uses dispatcher logic
from overlap_chunker import merge_with_overlap
from typing import List, Dict

INPUT_FILE = "/home/santiago/dummy-files-for-project-testing/dummy.py"

def main():
    # 1. Use dispatcher to get semantic chunks (tree-sitter or fallback)
    semantic_chunks = chunk_file(INPUT_FILE)

    if not semantic_chunks:
        print(f"[WARN] No blocks found in {INPUT_FILE}")
        return

    print(f"\n[INFO] Got {len(semantic_chunks)} semantic chunks from {os.path.basename(INPUT_FILE)}")

    # 2. Merge chunks with overlap for Qwen3-Embedding 8B
    # Target: 500-800 tokens per chunk
    final_chunks = merge_with_overlap(semantic_chunks)

    print(f"[INFO] Created {len(final_chunks)} final chunks for embedding")

    # 3. Output results
    print("\n" + "="*60)
    print("SEMANTIC CHUNKS (from tree-sitter/fallback):")
    print("="*60)
    
    #Edit to semantic_chunks[:3] to just show the first 3
    for i, block in enumerate(semantic_chunks, start=1):  # Show first 3
        print(f"\n--- Semantic Chunk {i} ---")
        print(f"Tokens: {block['tokens']}")
        content = block['content']
        print(content[:200] + "..." if len(content) > 200 else content)

    #if len(semantic_chunks) > 3:
    #    print(f"\n... and {len(semantic_chunks) - 3} more semantic chunks")

    print("\n" + "="*60)
    print("FINAL CHUNKS (for Qwen3-Embedding 8B):")
    print("="*60)

    for i, chunk in enumerate(final_chunks, start=1):
        print(f"\n--- Final Chunk {i} ---")
        print(f"Tokens: {chunk['tokens']}")
        print(f"Content:\n{chunk['content']}")
        print("-" * 50)

    # 4. Summary statistics
    print("\n" + "="*60)
    print("SUMMARY:")
    print("="*60)
    print(f"Original semantic chunks: {len(semantic_chunks)}")
    print(f"Total tokens in semantic chunks: {sum(c['tokens'] for c in semantic_chunks)}")
    print(f"Final merged chunks: {len(final_chunks)}")

    if final_chunks:
        total_tokens = sum(c['tokens'] for c in final_chunks)
        print(f"Average tokens per final chunk: {total_tokens / len(final_chunks):.1f}")

        token_counts = [c['tokens'] for c in final_chunks]
        print(f"Min tokens: {min(token_counts)}")
        print(f"Max tokens: {max(token_counts)}")

        in_range = [c for c in final_chunks if 500 <= c['tokens'] <= 800]
        below_range = [c for c in final_chunks if c['tokens'] < 500]
        above_range = [c for c in final_chunks if c['tokens'] > 800]

        print(f"\n[INFO] Token distribution:")
        print(f"  In target range (500-800): {len(in_range)} chunks")
        print(f"  Below 500 tokens: {len(below_range)} chunks")
        print(f"  Above 800 tokens: {len(above_range)} chunks")

        if len(in_range) == len(final_chunks):
            print("\n[SUCCESS] All chunks are within optimal range for Qwen3-Embedding 8B!")
        else:
            if below_range:
                print(f"\n[INFO] {len(below_range)} chunks below 500 tokens (couldn't merge more without breaking boundaries)")
            if above_range:
                print(f"\n[INFO] {len(above_range)} chunks above 800 tokens (single large semantic chunks)")

if __name__ == "__main__":
    main()

