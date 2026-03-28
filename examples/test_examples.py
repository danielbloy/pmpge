#!/usr/bin/env python3
"""
Script to execute all Python files in subdirectories of the examples folder.
This will loop through each subdirectory and run each Python file in turn.
"""

import subprocess
import sys
from pathlib import Path


def execute_python_file(file_path):
    """Execute a Python file and capture its output."""
    print(f"\n{'=' * 40}")
    print(f"Executing: {file_path.name}")
    print(f"{'=' * 40}")

    try:
        # Execute the Python file
        result = subprocess.run(
            [sys.executable, str(file_path)],
            cwd=file_path.parent,
            capture_output=True,
            text=True,
            timeout=10  # 10 second timeout per script
        )

        # Print stdout
        if result.stdout:
            print("Output:")
            print(result.stdout)

        # Print stderr if there are errors
        if result.stderr:
            print("Errors:")
            print(result.stderr)

        # Print return code
        if result.returncode != 0:
            print(f"Process exited with code: {result.returncode}")
        else:
            print("Process completed successfully!")

    except subprocess.TimeoutExpired:
        print("ERROR: Script timed out!")
    except Exception as e:
        print(f"ERROR: Failed to execute {file_path}: {e}")


def main():
    """Main function to loop through subdirectories and execute Python example files."""
    # Get the examples directory (current directory of this script)
    examples_dir = Path(__file__).parent
    print(f"Looking for subdirectories in: {examples_dir}")

    # Get all subdirectories, sorted for consistent execution order
    subdirectories = []
    for item in examples_dir.iterdir():
        if item.is_dir() and not item.name.startswith('.') and not item.name == '__pycache__':
            subdirectories.append(item)

    # Sort subdirectories by name to ensure consistent order
    subdirectories.sort(key=lambda x: x.name)

    if not subdirectories:
        print("No subdirectories found!")
        return

    print(f"Found {len(subdirectories)} subdirectories:")
    for subdir in subdirectories:
        print(f"  {subdir.name}")

    # Loop through each subdirectory
    for subdir in subdirectories:
        print(f"\n{'#' * 40}")
        print(f"Processing directory: {subdir.name}")
        print(f"{'#' * 40}")

        # Find all Python files in this subdirectory
        python_files = []
        for file_path in subdir.iterdir():
            if file_path.is_file() and file_path.suffix == '.py':
                if file_path.name != "a_template_game_loop.py":
                    python_files.append(file_path)

        # Sort Python files by name for consistent execution order
        python_files.sort(key=lambda x: x.name)

        if not python_files:
            print(f"No Python files found in {subdir.name}")
            continue

        print(f"Found {len(python_files)} Python files:")
        for py_file in python_files:
            print(f"  {py_file.name}")

        # Execute each Python file
        for py_file in python_files:
            execute_python_file(py_file)

    print(f"\n{'#' * 40}")
    print("All directories and files have been processed!")
    print(f"{'#' * 40}")


def test_examples():
    """
    Run all the examples in the test framework.
    """
    main()


if __name__ == "__main__":
    main()
