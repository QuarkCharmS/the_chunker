# overlap_chunker.py
"""
Creates overlapping chunks from semantic chunks for optimal embedding performance.
Designed for Qwen-3 embedding model with ~100 token overlap.
"""

from typing import List, Dict
from chunking.tokenizer import count_tokens  # Import the tokenizer from chunking module


def create_overlapping_chunks(
    semantic_chunks: List[Dict[str, any]], 
    target_size: int = 400,
    overlap_tokens: int = 100,
    max_chunk_size: int = 512
) -> List[Dict[str, any]]:
    """
    Create overlapping chunks from semantic chunks.
    
    Args:
        semantic_chunks: List of chunks from tree-sitter/fallback with 'content' and 'tokens' keys
        target_size: Target size for each chunk in tokens (default: 400)
        overlap_tokens: Number of tokens to overlap between chunks (default: 100)
        max_chunk_size: Maximum allowed chunk size (default: 512 for most embedding models)
    
    Returns:
        List of overlapping chunks with 'content', 'tokens', and 'metadata' keys
    """
    if not semantic_chunks:
        return []
    
    # First, flatten all content while keeping track of boundaries
    all_content = []
    chunk_boundaries = []  # (start_idx, end_idx, original_chunk_idx)
    current_pos = 0
    
    for idx, chunk in enumerate(semantic_chunks):
        content = chunk['content']
        tokens = chunk['tokens']
        
        all_content.append(content)
        chunk_boundaries.append((current_pos, current_pos + tokens, idx))
        current_pos += tokens
    
    # Join all content with newlines to preserve structure
    full_text = "\n\n".join(all_content)
    total_tokens = sum(chunk['tokens'] for chunk in semantic_chunks)
    
    print(f"[INFO] Creating overlapping chunks from {len(semantic_chunks)} semantic chunks")
    print(f"[INFO] Total tokens: {total_tokens}, target size: {target_size}, overlap: {overlap_tokens}")
    
    # If total content is smaller than target size, return as single chunk
    if total_tokens <= target_size:
        return [{
            'content': full_text,
            'tokens': total_tokens,
            'metadata': {
                'chunk_type': 'complete',
                'source_chunks': list(range(len(semantic_chunks)))
            }
        }]
    
    # Create overlapping chunks
    overlapping_chunks = []
    
    # Split the text into words for better chunking
    words = full_text.split()
    
    if not words:
        return []
    
    # Estimate tokens per word (rough approximation)
    avg_tokens_per_word = total_tokens / len(words) if words else 1
    words_per_chunk = int(target_size / avg_tokens_per_word)
    words_overlap = int(overlap_tokens / avg_tokens_per_word)
    
    print(f"[DEBUG] Estimated {avg_tokens_per_word:.2f} tokens per word")
    print(f"[DEBUG] Words per chunk: {words_per_chunk}, overlap: {words_overlap}")
    
    start_idx = 0
    chunk_num = 0
    
    while start_idx < len(words):
        # Calculate end index for this chunk
        end_idx = min(start_idx + words_per_chunk, len(words))
        
        # Extract chunk content
        chunk_words = words[start_idx:end_idx]
        chunk_content = " ".join(chunk_words)
        
        # Count actual tokens
        chunk_tokens = count_tokens(chunk_content)
        
        # If chunk is too large, reduce it
        while chunk_tokens > max_chunk_size and len(chunk_words) > 10:
            chunk_words = chunk_words[:-10]  # Remove 10 words at a time
            chunk_content = " ".join(chunk_words)
            chunk_tokens = count_tokens(chunk_content)
        
        # Determine which semantic chunks this overlaps with
        chunk_start_chars = len(" ".join(words[:start_idx])) if start_idx > 0 else 0
        chunk_end_chars = len(" ".join(words[:end_idx]))
        
        overlapping_chunks.append({
            'content': chunk_content,
            'tokens': chunk_tokens,
            'metadata': {
                'chunk_type': 'overlapping',
                'chunk_number': chunk_num,
                'start_word': start_idx,
                'end_word': end_idx,
                'total_words': len(words)
            }
        })
        
        chunk_num += 1
        
        # Move start index forward, considering overlap
        if end_idx >= len(words):
            break
        
        # Next chunk starts with overlap from current chunk
        start_idx = end_idx - words_overlap
        if start_idx <= 0:
            start_idx = end_idx  # Prevent infinite loop
    
    print(f"[INFO] Created {len(overlapping_chunks)} overlapping chunks")
    
    return overlapping_chunks


def create_sliding_window_chunks(
    text: str,
    window_size: int = 400,
    stride: int = 300,
    max_chunk_size: int = 512
) -> List[Dict[str, any]]:
    """
    Alternative method: Create chunks using a sliding window approach.
    
    Args:
        text: The full text to chunk
        window_size: Size of each chunk in tokens
        stride: How many tokens to move forward for each chunk (window_size - overlap)
        max_chunk_size: Maximum allowed chunk size
    
    Returns:
        List of overlapping chunks
    """
    words = text.split()
    if not words:
        return []
    
    total_tokens = count_tokens(text)
    avg_tokens_per_word = total_tokens / len(words)
    
    window_words = int(window_size / avg_tokens_per_word)
    stride_words = int(stride / avg_tokens_per_word)
    
    chunks = []
    start = 0
    
    while start < len(words):
        end = min(start + window_words, len(words))
        chunk_text = " ".join(words[start:end])
        chunk_tokens = count_tokens(chunk_text)
        
        # Ensure chunk isn't too large
        while chunk_tokens > max_chunk_size and end > start + 10:
            end -= 5
            chunk_text = " ".join(words[start:end])
            chunk_tokens = count_tokens(chunk_text)
        
        chunks.append({
            'content': chunk_text,
            'tokens': chunk_tokens,
            'metadata': {
                'method': 'sliding_window',
                'start': start,
                'end': end,
                'total_words': len(words)
            }
        })
        
        if end >= len(words):
            break
            
        start += stride_words
    
    return chunks


def process_file_with_overlap(
    semantic_chunks: List[Dict[str, any]],
    method: str = "overlap",
    **kwargs
) -> List[Dict[str, any]]:
    """
    Main entry point for creating overlapping chunks.
    
    Args:
        semantic_chunks: Chunks from tree-sitter or fallback chunker
        method: Either "overlap" or "sliding_window"
        **kwargs: Additional arguments for the specific method
    
    Returns:
        List of processed chunks ready for embedding
    """
    if not semantic_chunks:
        return []
    
    # Combine all semantic chunks into one text
    full_text = "\n\n".join(chunk['content'] for chunk in semantic_chunks)
    
    if method == "sliding_window":
        return create_sliding_window_chunks(full_text, **kwargs)
    else:
        return create_overlapping_chunks(semantic_chunks, **kwargs)

