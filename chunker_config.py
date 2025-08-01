LANG_FUNCTION_NODES = {
    # === High-level languages ===
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

    # === Scripting / shell ===
    "bash": {"function_definition"},
    "shell": {"function_definition"},
    "powershell": {"function_definition"},

    # === Infra / DevOps ===
    "yaml": {"block_mapping_pair"},              # e.g. GitLab CI jobs, scripts
    "json": {"pair"},                            # key-value pairs
    "toml": {"pair"},
    "ini": {"pair"},
    "dockerfile": {"instruction"},
    "gitlab_ci": {"block_mapping_pair"},
    "jenkinsfile": {"method_definition"},        # Groovy-style pipeline blocks
    "groovy": {"class_definition", "method_definition"},

    # === Markup / docs ===
    "html": {"element"},
    "xml": {"element"},
    "markdown": {"atx_heading", "fenced_code_block"},  # structure + code
    "md": {"atx_heading", "fenced_code_block"},

    # === Assembly / low-level ===
    "asm": {"label"},       # for GAS
    "nasm": {"label"},      # for NASM

    # === SQL ===
    "sql": {"select", "insert", "update", "create"},

    # === Fallback ===
    "default": {
        "function", "method", "function_definition",
        "procedure", "block", "section", "class", "module"
    }
}

EXT_TO_LANG = {
    # High-level programming languages
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".java": "java",
    ".cs": "c_sharp",
    ".rb": "ruby",
    ".go": "go",
    ".rs": "rust",

    # Low-level languages
    ".c": "c",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".h": "c",        # or cpp depending on context
    ".hpp": "cpp",
    ".s": "asm",
    ".asm": "nasm",
    ".S": "asm",

    # Shell + scripting
    ".sh": "bash",
    ".bash": "bash",
    ".zsh": "bash",  # fallback as bash
    ".ps1": "powershell",

    # Markup / documentation
    ".html": "html",
    ".htm": "html",
    ".xml": "xml",
    ".md": "markdown",
    ".markdown": "markdown",

    # Data / Config / Infra
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".toml": "toml",
    ".ini": "ini",
    ".env": "ini",   # for lack of a better fit
    ".properties": "ini",

    # SQL / DB
    ".sql": "sql",

    # CI/CD / DevOps
    ".gitlab-ci.yml": "yaml",         # GitLab CI
    ".gitlab-ci.yaml": "yaml",
    "Jenkinsfile": "groovy",          # Jenkins pipeline
    ".groovy": "groovy",
    "Dockerfile": "dockerfile",
    ".dockerfile": "dockerfile",
    ".dockerignore": "dockerfile",    # handled as config

    # Build / Package / Meta
    ".make": "make",                  # Not Tree-sitter supported (yet)
    "Makefile": "make",
    "CMakeLists.txt": "cmake",        # CMake config
    ".cmake": "cmake",

    # Misc
    ".txt": "markdown",               # fallback to markdown-like parsing
    ".log": "markdown",               # if needed, group by lines or sections
}
