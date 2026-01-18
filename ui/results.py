"""
Results display components.
"""

import streamlit as st
from typing import Dict


def render_status_card(result: Dict) -> None:
    """
    Render the beautiful status card based on analysis result.
    
    Args:
        result: Analysis result dictionary
    """
    status = result.get('status', 'CAUTION')
    
    if status == "SAFE":
        icon = "🛡️"
        status_class = "status-safe"
        status_label = "SAFE TO USE"
    elif status == "DANGER":
        icon = "🚨"
        status_class = "status-danger"
        status_label = "WARNING: DO NOT USE"
    else:  # CAUTION
        icon = "⚠️"
        status_class = "status-caution"
        status_label = "USE WITH CAUTION"
    
    st.markdown(f"""
    <div class="status-card {status_class}">
        <div class="status-icon">{icon}</div>
        <div class="status-text">{status_label}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Summary
    st.markdown("### 📋 Analysis Summary")
    st.info(result.get('summary', 'No summary available'))
    
    # Details
    details = result.get('details', [])
    if details:
        st.markdown("### 🔍 Details")
        for detail in details:
            st.markdown(f"- {detail}")
    
    # Recommendation
    st.markdown(f"""
    <div class="recommendation-box">
        <h4>💡 Pharmacist's Recommendation</h4>
        <p>{result.get('recommendation', 'Consult a healthcare professional.')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # PCCA Compounding Hook (The winning feature!)
    if result.get('compounding_suggested', False):
        st.markdown(f"""
        <div class="pcca-callout">
            <h4>🧪 Personalized Medicine Option</h4>
            <p>{result.get('compounding_note', 'A compounding pharmacist may be able to help.')}</p>
            <br>
            <p><strong>Find a PCCA-member pharmacy near you for custom formulations!</strong></p>
        </div>
        """, unsafe_allow_html=True)


def render_empty_results_placeholder() -> None:
    """
    Show placeholder when no results yet.
    """
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


def render_scanned_text_debug(scanned_text: str) -> None:
    """
    Show OCR text in expander for debugging.
    
    Args:
        scanned_text: The extracted text from OCR
    """
    with st.expander("🔤 View Scanned Text (Debug)"):
        st.code(scanned_text or "No text scanned yet")
