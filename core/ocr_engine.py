"""
OCR (Optical Character Recognition) engine using EasyOCR.
"""

import streamlit as st
import numpy as np
from PIL import Image
from typing import Union
from config.settings import OCR_LANGUAGE, OCR_GPU_ENABLED, OCR_VERBOSE


@st.cache_resource
def load_ocr_reader():
    """
    Load EasyOCR reader with GPU support if available.
    
    Returns:
        EasyOCR Reader instance or None if loading fails
    """
    try:
        import easyocr
        # GPU=True will auto-detect CUDA availability
        reader = easyocr.Reader(
            OCR_LANGUAGE,
            gpu=OCR_GPU_ENABLED,
            verbose=OCR_VERBOSE
        )
        return reader
    except Exception as e:
        st.error(f"Failed to load OCR engine: {e}")
        return None


def extract_text_from_image(image_data: Union[Image.Image, np.ndarray]) -> str:
    """
    Extract text from image using EasyOCR.
    
    Args:
        image_data: PIL Image or numpy array
        
    Returns:
        Extracted text as string
    """
    try:
        # Load OCR reader
        if st.session_state.ocr_reader is None:
            with st.spinner("🔧 Loading OCR engine (first time only)..."):
                st.session_state.ocr_reader = load_ocr_reader()
        
        reader = st.session_state.ocr_reader
        if reader is None:
            return "[OCR Engine unavailable]"
        
        # Convert PIL Image to numpy array
        if isinstance(image_data, Image.Image):
            img_array = np.array(image_data)
        else:
            img_array = image_data
        
        # Perform OCR
        with st.spinner("🔍 Scanning text from image..."):
            results = reader.readtext(img_array, detail=0, paragraph=True)
        
        # Join all detected text
        extracted_text = "\n".join(results)
        return extracted_text if extracted_text.strip() else "[No text detected]"
    
    except Exception as e:
        return f"[OCR Error: {str(e)}]"
