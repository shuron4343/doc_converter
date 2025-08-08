"""
Document Converter - конвертация документов в markdown с помощью docling
"""

__version__ = "0.1.0"
__author__ = "Document Converter Team"

from .converter import DocumentConverter
from .cli import main

__all__ = ["DocumentConverter", "main"]
