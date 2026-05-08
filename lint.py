#!/usr/bin/env python3
"""Lint tool for Gomoku project structure and layer dependencies."""

import ast
import sys
from pathlib import Path


LAYERS = ["types", "config", "repo", "service", "runtime", "ui", "providers", "utils"]

STDLIB_MODULES = {
    "abc", "argparse", "ast", "asyncio", "base64", "collections", "contextlib",
    "copy", "csv", "dataclasses", "datetime", "decimal", "enum", "functools",
    "gzip", "hashlib", "heapq", "hmac", "html", "http", "imaplib", "inspect",
    "io", "itertools", "json", "linecache", "logging", "math", "mimetypes",
    "os", "pathlib", "pickle", "platform", "pprint", "queue", "random", "re",
    "select", "shutil", "signal", "smtplib", "socket", "socketserver", "sre",
    "ssl", "string", "struct", "subprocess", "sys", "tempfile", "textwrap",
    "threading", "time", "timer", "trace", "traceback", "types", "typing",
    "unittest", "urllib", "uuid", "warnings", "weakref", "xml", "xmlrpc",
    "zipfile", "zipimport", "zlib"
}

LAYER_PERMISSIONS = {
    "types": {"types"},
    "config": {"types", "config"},
    "repo": {"types", "config", "repo"},
    "service": {"types", "config", "repo", "providers", "service"},
    "runtime": {"types", "config", "repo", "service", "providers", "runtime"},
    "ui": {"types", "config", "service", "runtime", "providers", "ui"},
    "providers": {"types", "config", "utils", "providers"},
    "utils": {"utils"},
}


def get_layer(file_path: Path) -> str | None:
    """Return the layer name if file is in a layer directory, None otherwise."""
    try:
        rel_path = file_path.relative_to(Path("src"))
        parts = rel_path.parts
        if parts and parts[0] in LAYERS:
            return parts[0]
    except ValueError:
        pass
    return None


def get_imports(file_path: Path) -> list[tuple[str, int, int]]:
    """Parse file and return list of (module_name, line_number, level) for imports."""
    imports = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source, filename=str(file_path))
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append((alias.name, node.lineno, 0))
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append((node.module, node.lineno, node.level))
    except SyntaxError:
        pass
    return imports


def get_import_base(import_name: str) -> str:
    """Get the base module name (first part of dotted import)."""
    return import_name.split(".")[0]


def is_stdlib_module(module_name: str) -> bool:
    """Check if module is a standard library module."""
    base = get_import_base(module_name)
    return base in STDLIB_MODULES


def get_layer_from_module(module_name: str, level: int, current_layer: str) -> str | None:
    """Determine which layer an import refers to based on import style."""
    if level > 0:
        return current_layer
    base = get_import_base(module_name)
    if base == "src":
        parts = module_name.split(".")
        if len(parts) >= 2 and parts[1] in LAYERS:
            return parts[1]
        return None
    if base in LAYERS:
        return base
    return None


def check_file(file_path: Path) -> list[str]:
    """Check a single file and return list of error messages."""
    errors = []
    
    current_layer = get_layer(file_path)
    if current_layer is None:
        return errors
    
    imports = get_imports(file_path)
    allowed = LAYER_PERMISSIONS[current_layer]
    
    for module_name, lineno, level in imports:
        if is_stdlib_module(module_name):
            continue
        
        imported_layer = get_layer_from_module(module_name, level, current_layer)
        
        if imported_layer is None:
            continue
        
        if imported_layer not in allowed:
            errors.append(
                f"{file_path}:{lineno}: import '{module_name}' from disallowed layer '{imported_layer}'"
            )
    
    return errors


def check_line_count(file_path: Path) -> list[str]:
    """Check line count and return list of error messages."""
    errors = []
    
    layer = get_layer(file_path)
    if layer is None:
        return errors
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        line_count = len(lines)
        if line_count > 300:
            errors.append(
                f"{file_path}: line count ({line_count}) exceeds 300"
            )
    except (IOError, UnicodeDecodeError):
        pass
    
    return errors


def find_all_source_files() -> list[Path]:
    """Find all Python files under src/."""
    src_dir = Path("src")
    return list(src_dir.rglob("*.py"))


def main() -> int:
    """Run lint checks and return exit code."""
    errors = []
    
    files = find_all_source_files()
    
    for file_path in files:
        layer = get_layer(file_path)
        if layer is None:
            continue
        
        errors.extend(check_file(file_path))
        errors.extend(check_line_count(file_path))
    
    if errors:
        for error in errors:
            print(error)
        return 1
    
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
