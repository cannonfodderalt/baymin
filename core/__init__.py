"""
Core functionality for Contra-Scan.
"""

from .ocr_engine import load_ocr_reader, extract_text_from_image
from .ai_analyzer import analyze_safety, get_demo_response

__all__ = [
    'load_ocr_reader',
    'extract_text_from_image',
    'analyze_safety',
    'get_demo_response'
]
