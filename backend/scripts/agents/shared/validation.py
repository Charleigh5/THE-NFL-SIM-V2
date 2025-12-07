#!/usr/bin/env python3
"""
Shared Validation Utilities for Agent Scripts
==============================================
Validates generated code before marking outputs complete.

Context7 Best Practices:
- Syntax validation with py_compile
- Import validation
- File existence checks
"""

import py_compile
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple


def validate_python_syntax(file_path: Path) -> Tuple[bool, str]:
    """
    Validate Python file syntax.

    Args:
        file_path: Path to Python file

    Returns:
        Tuple of (success, error_message)
    """
    try:
        py_compile.compile(str(file_path), doraise=True)
        return True, ""
    except py_compile.PyCompileError as e:
        return False, str(e)


def validate_imports(file_path: Path) -> Tuple[bool, str]:
    """
    Validate that a Python file can be imported.

    Args:
        file_path: Path to Python file

    Returns:
        Tuple of (success, error_message)
    """
    try:
        result = subprocess.run(
            [sys.executable, "-c", f"import sys; sys.path.insert(0, '{file_path.parent}'); import {file_path.stem}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return True, ""
        else:
            return False, result.stderr
    except subprocess.TimeoutExpired:
        return False, "Import timed out"
    except Exception as e:
        return False, str(e)


def validate_files_exist(paths: List[Path]) -> Tuple[bool, List[Path]]:
    """
    Validate that all specified files exist.

    Args:
        paths: List of paths to check

    Returns:
        Tuple of (all_exist, missing_paths)
    """
    missing = [p for p in paths if not p.exists()]
    return len(missing) == 0, missing


def run_tests(test_path: Path) -> Tuple[bool, str]:
    """
    Run pytest on specified test file.

    Args:
        test_path: Path to test file or directory

    Returns:
        Tuple of (success, output)
    """
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(test_path), "-v", "--tb=short"],
            capture_output=True,
            text=True,
            timeout=120
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "Tests timed out"
    except Exception as e:
        return False, str(e)
