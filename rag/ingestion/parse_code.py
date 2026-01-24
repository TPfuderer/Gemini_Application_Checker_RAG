"""
Extract function-level knowledge units from Python source code.

Design choice:
- One function = one chunk
- Uses Python AST (robust, not regex-based)
- Read-only analysis (no execution)

This enables precise, explainable retrieval in RAG.
"""

import ast
from typing import List, Dict


def extract_functions(code: str) -> List[Dict]:
    """
    Parse Python source code and extract function definitions.

    Returns a list of dicts with:
    - name: function name
    - start_line: starting line number (0-based)
    - end_line: ending line number (exclusive)
    """
    try:
        tree = ast.parse(code)
    except SyntaxError:
        # Skip files that cannot be parsed safely
        return []

    functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if node.end_lineno is None:
                continue

            functions.append({
                "name": node.name,
                "start_line": node.lineno - 1,
                "end_line": node.end_lineno,
            })

    return functions
