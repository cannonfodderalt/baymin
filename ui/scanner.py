"""
Product scanner interface component.
"""

import streamlit as st
from PIL import Image
from typing import Optional


def render_scanner_interface() -> Optional[Image.Image]:
    """
    Render the product scanner interface (camera + file upload).
    
    Returns:
        PIL.Image or None: Captured/uploaded image
    """
    st.markdown("### 📸 Scan Product Label")
    st.markdown("Point your camera at a medication bottle, food label, or supplement.")
    
    # Camera input
    camera_image = st.camera_input(
        "Take a photo of the product label",
        key="scanner",
        label_visibility="collapsed"
    )
    
    # Alternative: File upload
    st.markdown("**Or upload an image:**")
    uploaded_file = st.file_uploader(
        "Upload label image",
        type=['png', 'jpg', 'jpeg'],
        label_visibility="collapsed"
    )
    
    # Process image
    image_to_process = None
    if camera_image is not None:
        image_to_process = Image.open(camera_image)
    elif uploaded_file is not None:
        image_to_process = Image.open(uploaded_file)
    
    if image_to_process is not None:
        # Show captured image
        st.image(image_to_process, caption="Captured Label", use_container_width=True)
        return image_to_process
    
    return None
