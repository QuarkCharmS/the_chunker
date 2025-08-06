# the_chunker

A standalone chunking engine designed to process source code and other text files into semantically meaningful, token-aware chunks. It supports both AST-based and fallback strategies, with optional overlapping for context preservation.

---

## 🚀 Purpose

`the_chunker` is built to split input files into chunks optimized for large language model pipelines (e.g. RAG systems), but is fully decoupled from embedding or vector database logic. It supports:

- Tree-sitter based AST chunking
- Fallback chunking for unsupported formats
- Overlap-aware chunk merging
- Token counting for models like Qwen3

---

## 🧱 Project Structure

```
.
├── chunker.py                 # Entry point for running the chunking process
├── chunker-venv/              # Local Python virtual environment (excluded in .gitignore)
├── chunking/                  # Core logic module
│   ├── chunker_config.py      # Configuration values (token limits, model settings)
│   ├── dispatcher.py          # Selects tree_chunker or fallback_chunker per file
│   ├── fallback_chunker.py    # Fallback strategy for non-code files
│   ├── tokenizer.py           # Token counting utilities
│   ├── tree_chunker.py        # Tree-sitter based AST chunker
│   ├── chunking-logic.md      # Developer notes on chunking strategy
│   └── __init__.py
├── my_overlap_chunker.py      # Experimental overlap strategy (WIP)
├── start-everything.sh        # Activation script for environment
├── requirements-wheel.txt     # Dependencies to install from wheel (airgapped)
├── README.md                  # You're here
├── .gitignore                 # Clean repo by ignoring common files
└── wheels/                    # Pre-downloaded .whl files for offline setup
```

---

## ⚙️ Setup

```bash
source start-everything.sh
```

This activates your virtual environment (`chunker-venv`) and sets up the working shell.

If you're setting up from scratch (e.g. on a fresh machine), install dependencies like so:

```bash
python3 -m venv chunker-venv
source chunker-venv/bin/activate
pip install --no-index --find-links=./wheels -r requirements-wheel.txt
```

---

## 🧪 Usage

Example usage:

```python
from chunking.dispatcher import chunk_file

chunks = chunk_file("path/to/codefile.py")
for chunk in chunks:
    print(f"{chunk['tokens']} tokens\n---\n{chunk['content']}\n")
```

You can also call `merge_with_overlap()` manually on semantic chunks if needed (from `my_overlap_chunker.py` or `fallback_chunker.py`).

---

## ✅ Features

- Tree-sitter support for Python, JavaScript, TypeScript, etc.
- Clean fallback for plaintext or unknown file types
- Configurable token thresholds (e.g., target 500–800 tokens)
- Optional overlapping logic to preserve context
- Deterministic output for reproducibility
