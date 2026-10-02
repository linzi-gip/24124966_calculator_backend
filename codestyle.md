# Backend Code Style

> **Source**: [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/)
> (The official Python recommended code style standard)

The Python code in this project follows PEP 8. Below are the core conventions relevant to this project.

## 1. Indentation

- Use **4 spaces** per indentation level. Tabs are not allowed.

## 2. Line Length

- Limit lines to **79 characters**; long expressions and strings may go up to 99 characters.
- Break long statements with parentheses or backslashes.

## 3. Blank Lines

- Surround top-level functions and class definitions with **two** blank lines.
- Method definitions inside a class are separated by **one** blank line.

## 4. Naming Conventions

| Object | Style | Example |
| --- | --- | --- |
| Variables | lowercase with underscores | `expression` |
| Functions | lowercase with underscores | `evaluate_expression` |
| Classes | PascalCase | `Parser`, `Database` |
| Constants | UPPER_CASE with underscores | `DB_PATH` |
| Private methods | leading underscore | `_connect()` |

## 5. Quotes

- Prefer single quotes for strings; use double quotes when the string contains a single quote.

## 6. Comments and Docstrings

- Every module, class, and function should have a docstring explaining its purpose and parameters.
- Comments may be in English or Chinese; this project uses English.

## 7. Imports

- One import per line.
- Import order: standard library → third-party → local modules, each group separated by a blank line.

## 8. Whitespace

- One space around operators: `value = a + b`
- One space after commas: `func(a, b)`
- No extra spaces inside parentheses: `func(a, b)` not `func( a, b )`
- No spaces around the `=` in keyword arguments: `func(key=value)`

## 9. Exception Handling

- Catch specific exception types (e.g., `ValueError`, `ZeroDivisionError`); avoid bare `except:`.
- Custom exceptions inherit from built-in exceptions such as `ValueError`.

## 10. Other

- Keep a single trailing newline at the end of each file.
- Use `# -*- coding: utf-8 -*-` at the top of files to ensure non-ASCII strings work correctly.
