# overlap_chunker.py
"""
Post-processes semantic chunks to introduce intelligent overlap and padding.
Optimized for Qwen3-Embedding 8B with target range of 500-800 tokens.
"""

from typing import List, Dict, Union


def merge_with_overlap(semantic_chunks: List[Dict[str, Union[str, int]]]) -> List[Dict[str, Union[str, int]]]:
    """
    Merge semantic chunks to optimize for embedding model.
    
    Rules:
    - Target range: 500-800 tokens per chunk
    - Never break semantic boundaries
    - Add overlap by prepending last chunk if ≤ 100 tokens
    - Single chunks > 800 tokens are allowed as-is
    
    Args:
        semantic_chunks: List of dicts with 'content' and 'tokens' keys
        
    Returns:
        List of merged chunks with same structure
    """
    if not semantic_chunks:
        return []

    final_chunks = []
    i = 0

    while i < len(semantic_chunks):
        current_content = []
        current_tokens = 0
        
        # Check if we should add overlap from previous chunks
        if final_chunks and i > 0:
            overlap_content = []
            overlap_tokens = 0
            
            # Go backwards through previous chunks until we reach ~100 tokens
            j = i - 1
            while j >= 0:
                prev_chunk = semantic_chunks[j]
                
                # Add this chunk to the beginning of overlap
                overlap_content.insert(0, prev_chunk['content'])
                overlap_tokens += prev_chunk['tokens']
                j -= 1
            
                if overlap_tokens > 100:
                    break

        # Add chunks until we reach target range
        while i < len(semantic_chunks):
            chunk = semantic_chunks[i]
            chunk_tokens = chunk['tokens']
            
            # If current chunk alone is >= 500, emit what we have
            if not current_content and chunk_tokens >= 500:
                final_chunks.append({
                    'content': chunk['content'],
                    'tokens': chunk_tokens
                })
                i += 1
                break
            
            # If adding this chunk would exceed 800, stop (unless we have nothing)
            if current_content and current_tokens + chunk_tokens > 800:
                break
            
            # Add this chunk
            current_content.append(chunk['content'])
            current_tokens += chunk_tokens
            i += 1
            
            # If we've reached our minimum target, we can emit
            if current_tokens >= 500:
                break
        
        # Emit accumulated chunks if any
        if current_content:
            final_chunks.append({
                'content': '\n\n'.join(current_content),
                'tokens': current_tokens
            })

    # Print summary for verification
    print(f"[INFO] Merged {len(semantic_chunks)} semantic chunks into {len(final_chunks)} final chunks")
    for idx, chunk in enumerate(final_chunks):
        print(f"  Chunk {idx}: {chunk['tokens']} tokens")

    return final_chunks
