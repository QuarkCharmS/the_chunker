## Chunking Logic – Tree Splitter with Overlap

Each file is split using a tree-based approach where the code is parsed into logical blocks (e.g. functions, classes). These blocks are emitted as base chunks.

Chunks are then grouped into final windows using a sliding window with **overlap** to preserve context between chunks.

### Logic Summary

1. **Parse code** into tree blocks (classes, functions, etc.)
2. **Flatten** the tree into a list of base chunks (raw text)
3. **Group** base chunks into final chunks using:
   - `chunk_size` → max number of base chunks per window
   - `chunk_overlap` → number of base chunks to repeat from previous window

4. Emit each final chunk with its content and UUIDv5 (based on path + content)

This keeps chunks semantically meaningful **and** preserves cross-chunk context.

## Detailed Behavior

The chunker operates in two main phases:

### 1. Tree-Based Splitting
- Parses each source file into a hierarchy of code blocks using a syntax parser.
- Only meaningful blocks (functions, methods, classes) are extracted.
- Ignores whitespace, comments, and very short or empty blocks.
- Output: a flat, ordered list of **base chunks** (not raw lines—actual logical units).

### 2. Overlapping Windowing
- Walks through the base chunk list and creates windows of size `chunk_size`.
- Each window overlaps the previous one by `chunk_overlap` elements.
- Ensures context continuity between adjacent chunks (e.g. function A's end + function B's start).
- Handles edge cases at the beginning and end of the list cleanly.
- Example: with `chunk_size=4`, `chunk_overlap=2`, you get:
  - `[0,1,2,3]`
  - `[2,3,4,5]`
  - `[4,5,6,7]`  
  ...and so on.

### Output
Each final chunk includes:
- The concatenated content of grouped base chunks
- A deterministic UUIDv5 hash (from file path + chunk content)
- The source file path
- Optionally: line span or block indices

This setup maximizes semantic precision and contextual relevance for downstream embedding and retrieval.

