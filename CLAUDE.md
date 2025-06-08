# CTF Utilities Repository

This repository contains a collection of useful tools and utilities for Capture The Flag (CTF) competitions.

## Repository Overview

This is a CTF utilities repository that provides various tools to help with CTF challenges including:

- Web exploitation tools
- Cryptography helpers
- Binary analysis utilities
- Network analysis scripts
- Miscellaneous CTF problem-solving tools

## Directory Structure

- `server/` - Web server utilities and tools for web-based CTF challenges
  - `app.py` - Flask application for serving static and dynamic content
  - `static/` - Static files directory
  - `js/` - JavaScript utilities
- `pwntools-examples/` - Pwntools usage examples for binary exploitation
  - `pwntools_examples.ipynb` - Jupyter notebook with comprehensive pwntools examples including:
    - Basic I/O operations and connections
    - Packing/unpacking data
    - Buffer overflow examples
    - ROP (Return Oriented Programming)
    - Format string attacks
    - Shellcode execution
    - Heap exploitation basics
    - GDB debugging integration
    - Cryptographic utilities
    - Useful CTF utilities

## Development Guidelines

When contributing to this repository:

1. Keep tools modular and reusable
2. Add clear documentation for each utility
3. Include usage examples where appropriate
4. Test tools before committing

## Testing

Before committing changes, ensure code quality by running:

- Python linting: `ruff check .` (if available)
- JavaScript linting: Check individual tool directories for linting commands

## Security Note

This repository is specifically for CTF competition use. Tools here are designed for educational purposes and authorized security testing only.

## Memories

- to memorize 