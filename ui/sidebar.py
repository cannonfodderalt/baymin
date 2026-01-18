"""
Medical profile sidebar component.
"""

import streamlit as st
from typing import Dict
from config.settings import DEMO_MODE


def render_medical_profile_sidebar() -> Dict[str, str]:
    """
    Render the medical profile sidebar.
    
    Returns:
        dict: {
            'prescriptions': str,
            'allergies': str,
            'conditions': str,
            'is_complete': bool
        }
    """
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header">
            <h3>👤 Your Medical Profile</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("Enter your information for personalized safety checks.")
        
        # Prescriptions
        st.markdown('<div class="profile-section">', unsafe_allow_html=True)
        st.markdown("**💊 Current Prescriptions**")
        prescriptions = st.text_area(
            "List your medications (comma-separated)",
            placeholder="e.g., Warfarin, Lisinopril, Metformin",
            key="prescriptions",
            height=80,
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Allergies
        st.markdown('<div class="profile-section">', unsafe_allow_html=True)
        st.markdown("**🚫 Known Allergies**")
        allergies = st.text_area(
            "List allergies (comma-separated)",
            placeholder="e.g., Peanuts, Red Dye 40, Penicillin",
            key="allergies",
            height=80,
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Medical Conditions
        st.markdown('<div class="profile-section">', unsafe_allow_html=True)
        st.markdown("**🏥 Medical Conditions**")
        conditions = st.text_area(
            "List conditions (comma-separated)",
            placeholder="e.g., Hypertension, Diabetes Type 2",
            key="conditions",
            height=80,
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Profile summary
        st.markdown("---")
        st.markdown("**📊 Profile Status**")
        profile_complete = bool(prescriptions or allergies or conditions)
        if profile_complete:
            st.success("✅ Profile configured")
        else:
            st.warning("⚠️ Add your info for personalized analysis")
        
        # Demo mode indicator
        st.markdown("---")
        if DEMO_MODE:
            st.markdown("""
            <div style="background: #FF6F00; padding: 0.5rem; border-radius: 5px; text-align: center;">
                <span style="color: white; font-weight: bold;">🎮 DEMO MODE</span>
            </div>
            """, unsafe_allow_html=True)
            st.caption("Set GEMINI_API_KEY environment variable for live AI analysis")
        else:
            st.markdown("""
            <div style="background: #4CAF50; padding: 0.5rem; border-radius: 5px; text-align: center;">
                <span style="color: white; font-weight: bold;">🤖 AI ACTIVE</span>
            </div>
            """, unsafe_allow_html=True)
            st.caption("Powered by Google Gemini")
    
    return {
        'prescriptions': prescriptions,
        'allergies': allergies,
        'conditions': conditions,
        'is_complete': profile_complete
    }
