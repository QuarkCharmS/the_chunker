# chunker_config.py

# === Node types to extract per language (Tree-sitter based) ===
LANG_FUNCTION_NODES = {
    # High-level languages
    "python": {"function_definition", "class_definition"},
    "javascript": {"function_declaration", "method_definition", "arrow_function"},
    "typescript": {"function_declaration", "method_definition", "arrow_function"},
    "java": {"class_declaration", "method_declaration"},
    "c": {"function_definition"},
    "cpp": {"function_definition", "class_specifier"},
    "c_sharp": {"class_declaration", "method_declaration"},
    "go": {"function_declaration", "method_declaration"},
    "rust": {"function_item", "impl_item"},
    "ruby": {"class", "module", "method"},

    # Shell / scripting
    "bash": {"function_definition"},
    "shell": {"function_definition"},
    "powershell": {"function_definition"},

    # Groovy-based CI pipelines
    "groovy": {"class_definition", "method_definition"},
    "jenkinsfile": {"method_definition"},

    # Assembly / low-level
    "asm": {"label"},     # GAS style
    "nasm": {"label"},    # NASM style

    # SQL
    "sql": {"select", "insert", "update", "create"},

    # Fallback
    "default": {
        "function", "method", "function_definition",
        "procedure", "block", "section", "class", "module"
    }
}

# === File extension to language mapping ===
EXT_TO_LANG = {
    # High-level
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".java": "java",
    ".cs": "c_sharp",
    ".rb": "ruby",
    ".go": "go",
    ".rs": "rust",

    # Low-level
    ".c": "c",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".h": "c",
    ".hpp": "cpp",
    ".s": "asm",
    ".S": "asm",
    ".asm": "nasm",

    # Shell
    ".sh": "bash",
    ".bash": "bash",
    ".zsh": "bash",
    ".ps1": "powershell",

    # Markup / docs
    ".html": "html",
    ".htm": "html",
    ".xml": "xml",
    ".md": "markdown",
    ".markdown": "markdown",

    # Data / config / infra
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".toml": "toml",
    ".ini": "ini",
    ".env": "ini",
    ".properties": "ini",

    # CI/CD
    ".gitlab-ci.yml": "yaml",
    ".gitlab-ci.yaml": "yaml",
    ".groovy": "groovy",
    "Jenkinsfile": "groovy",
    "Dockerfile": "dockerfile",
    ".dockerfile": "dockerfile",
    ".dockerignore": "dockerfile",

    # Build systems
    ".make": "make",
    "Makefile": "make",
    "CMakeLists.txt": "cmake",
    ".cmake": "cmake",

    # SQL
    ".sql": "sql",

    # Misc (non-code fallback to markdown)
    ".txt": "markdown",
    ".log": "markdown",

    # Non-chunkable formats (map only for recognition)
    ".asl": "asl",
    ".m4": "m4",
}

# === Languages that can be chunked semantically using Tree-sitter ===
CHUNKABLE_LANGUAGES = {
    "python",
    "javascript",
    "typescript",
    "java",
    "c",
    "cpp",
    "c_sharp",
    "go",
    "rust",
    "ruby",
    "bash",
    "shell",
    "powershell",
    "groovy"
}
