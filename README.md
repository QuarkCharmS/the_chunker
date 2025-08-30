# the\_chunker

A standalone chunking engine that turns source code and other text files into **semantically meaningful, token‑aware chunks**. It supports AST‑based chunking via Tree‑sitter and robust fallbacks for everything else, plus optional overlap merging tuned for embedding models.

---

## 🚀 What it's for

`the_chunker` splits input files into chunks optimized for LLM pipelines (RAG, summarization, code search) while staying **decoupled from embedding/vector DB logic**.

Core capabilities:

- Tree‑sitter based AST chunking
- Fallback chunking for unsupported formats
- Overlap‑aware merging to preserve context windows
- Token counting (model‑aware) with configurable targets

---

## 🧱 Project Structure

```
.
├── src/
│   └── the_chunker/           # Main package
│       ├── __init__.py        # Package initialization
│       ├── chunker.py         # Main entry point for running chunking locally
│       ├── my_overlap_chunker.py  # Overlap strategy (tuned for Qwen3‑Embedding 8B)
│       └── chunking/          # Core logic module
│           ├── __init__.py
│           ├── chunker_config.py    # Token limits, model settings, feature flags
│           ├── dispatcher.py        # Chooses tree_chunker or fallback_chunker per file
│           ├── fallback_chunker.py  # Fallback strategy for non‑code files
│           ├── tokenizer.py         # Token counting utilities (HF/other tokenizers)
│           ├── tree_chunker.py      # Tree‑sitter AST chunker
│           └── chunking-logic.md    # Developer notes on chunking strategy
├── pyproject.toml             # Modern Python packaging configuration
├── test_chunker.py            # Test file
├── README.md                  # Project documentation
└── .gitignore                 # Clean repo ignores
```

---

## ⚙️ Setup

Install the package:

```bash
# Install in editable mode for development
pip install -e .

# Or install directly from GitHub
pip install git+https://github.com/QuarkCharmS/the_chunker.git
```

---

## 🧪 Python API

### High‑level helper

Use a single call to go from file → semantic blocks → merged final chunks.

```python
from the_chunker import turn_file_to_chunks

final_chunks = turn_file_to_chunks(
    input_file="/path/to/file.py",
    debug_level="VERBOSE",          # "NONE" or "VERBOSE"
    model_name="Qwen/Qwen3-Embedding-8B"  # affects token counting + merge targets
)
```

**What it does:**

1. `chunk_file()` builds **semantic chunks** using Tree‑sitter (when supported) or a fallback.
2. `merge_with_overlap()` combines adjacent blocks to hit target token ranges while preserving context with overlaps (tuned by `chunker_config.py`).

**Returns:** `List[Dict]` of chunk dicts like:

```python
{
  "content": str,              # chunk text
  "tokens": int,               # token count for chosen model
  "overlap_tokens": int,       # overlap size with neighbor (if any)
  # optional: other metadata added by chunkers
}
```

### Low‑level (semantic only)

```python
from the_chunker.chunking.dispatcher import chunk_file
semantic_chunks = chunk_file("path/to/codefile.py", model_name="Qwen/Qwen3-Embedding-8B")
```

### Manual merge

```python
from the_chunker import merge_with_overlap
final_chunks = merge_with_overlap(semantic_chunks)
```

### Debug output

Set `debug_level="VERBOSE"` in `turn_file_to_chunks(...)` to print:

- counts of semantic & final chunks
- token distribution vs target range
- previews of semantic and final chunk content

---

## 🎯 Token Targets & Overlap Strategy

Defaults are tuned for **Qwen3‑Embedding 8B**:

- **Target tokens per final chunk:** 500–800
- Overlap is applied between neighbors to preserve cross‑chunk context
- Large semantic blocks may exceed the upper bound by design (no hard wrap to avoid breaking AST/paragraph boundaries)

These thresholds live in `the_chunker/chunking/chunker_config.py`. Adjust to fit your model/context window.

---

## 🔢 Tokenization & Models

`tokenizer.py` resolves a tokenizer based on `model_name`:

- Works with **Hugging Face** tokenizer identifiers (e.g., `"Qwen/Qwen3-Embedding-8B"`, `"meta-llama/Llama-3-70b-hf"`).
- You can add aliases or custom logic in `chunker_config.py` to map model names → tokenizer names.
- If a tokenizer isn't found, we fall back to a reasonable default and log a warning.

> **Counting only**: The `model_name` is used to choose a tokenizer for **token counting**, not to call a remote API. Bring‑your‑own embedding/generation stack separately.

---

## 📦 Expected Output Shape

Both semantic and final chunks are Python dicts. The most common keys used by the pipeline:

| Key              | Type | Description                                            |
| ---------------- | ---- | ------------------------------------------------------ |
| `content`        | str  | The chunk text                                         |
| `tokens`         | int  | Token count under the active tokenizer                 |
| `overlap_tokens` | int  | Overlap size with the next/previous chunk (final pass) |

> Some chunkers may attach extra metadata (e.g., function/class names, file offsets). Treat unknown keys as optional.

---

## 🔎 Example: end‑to‑end

```python
from the_chunker import turn_file_to_chunks

chunks = turn_file_to_chunks("/home/user/project/main.py", debug_level="VERBOSE",
                             model_name="Qwen/Qwen3-Embedding-8B")
for i, c in enumerate(chunks, 1):
    print(f"#[{i}] tokens={c['tokens']} overlap={c.get('overlap_tokens', 0)}\n{c['content'][:200]}…\n")
```

---
