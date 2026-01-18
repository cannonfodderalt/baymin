"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              CONTRA-SCAN                                       ║
║           Personalized Medication Safety Scanner for Complex Patients          ║
║                                                                                 ║
║   🏆 nwHacks 2026 - [PCCA] Best Wellness Related Hack                         ║
║   🤖 [MLH] Best Use of Gemini                                                  ║
╚═══════════════════════════════════════════════════════════════════════════════╝

Main Streamlit application entry point.
"""

import streamlit as st
from config.settings import DEMO_MODE
from ui import (
    get_custom_css,
    render_medical_profile_sidebar,
    render_scanner_interface,
    render_status_card,
    render_empty_results_placeholder,
    render_scanned_text_debug
)
from core import extract_text_from_image, analyze_safety

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG - Must be first Streamlit command
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Contra-Scan | Medication Safety",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════════════════════
# CUSTOM CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(get_custom_css(), unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# INITIALIZE SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
if 'ocr_reader' not in st.session_state:
    st.session_state.ocr_reader = None
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'scanned_text' not in st.session_state:
    st.session_state.scanned_text = None

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR - Medical Profile Input
# ══════════════════════════════════════════════════════════════════════════════
user_profile = render_medical_profile_sidebar()


# ══════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT AREA
# ══════════════════════════════════════════════════════════════════════════════

# Header
st.markdown("""
<div class="main-header">
    <h1>🛡️ Contra-Scan</h1>
    <p>Personalized Medication & Food Safety Scanner</p>
</div>
""", unsafe_allow_html=True)

# Demo mode banner
if DEMO_MODE:
    st.markdown("""
    <div class="demo-banner">
        <p>🎮 DEMO MODE ACTIVE - Using simulated AI responses for demonstration</p>
    </div>
    """, unsafe_allow_html=True)

# Create two columns for layout
col1, col2 = st.columns([1, 1])

with col1:
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
        
        # Extract text button
        if st.button("🔍 Analyze Product", type="primary", use_container_width=True):
            # Build user profile
            user_profile = {
                "prescriptions": prescriptions,
                "allergies": allergies,
                "conditions": conditions
            }
            
            # Step 1: Extract text
            extracted_text = extract_text_from_image(image_to_process)
            st.session_state.scanned_text = extracted_text
            
            # Step 2: Analyze with AI
            if extracted_text and not extracted_text.startswith("["):
                with st.spinner("🧠 AI analyzing for safety concerns..."):
                    result = analyze_safety(user_profile, extracted_text)
                    st.session_state.analysis_result = result
            else:
                st.session_state.analysis_result = {
                    "status": "CAUTION",
                    "summary": "Could not read text from image clearly.",
                    "details": ["OCR extraction failed or returned empty"],
                    "recommendation": "Please try taking a clearer photo with better lighting.",
                    "compounding_suggested": False,
                    "compounding_note": ""
                }

with col2:
    st.markdown("### 📊 Safety Analysis Results")
    
    if st.session_state.analysis_result is not None:
        render_status_card(st.session_state.analysis_result)
        
        # Show scanned text in expander for debugging
        with st.expander("🔤 View Scanned Text (Debug)"):
            st.code(st.session_state.scanned_text or "No text scanned yet")
    else:
        st.markdown("""
        <div style="
            border: 2px dashed #444;
            border-radius: 15px;
            padding: 3rem;
            text-align: center;
            color: #888;
        ">
            <p style="font-size: 3rem; margin-bottom: 1rem;">📋</p>
            <p style="font-size: 1.2rem;">Scan a product to see safety analysis</p>
            <p style="font-size: 0.9rem; color: #666;">Results will appear here</p>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p><strong>Contra-Scan</strong> | nwHacks 2026 | Targeting PCCA Best Wellness Hack</p>
    <p style="font-size: 0.8rem;">⚠️ Disclaimer: This tool is for educational purposes only and does not replace professional medical advice. Always consult a healthcare provider or pharmacist.</p>
</div>
""", unsafe_allow_html=True)
