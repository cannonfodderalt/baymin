"""
Configuration settings for Contra-Scan application.
"""

import os

# ══════════════════════════════════════════════════════════════════════════════
# API CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
DEMO_MODE = not GEMINI_API_KEY
GEMINI_MODEL = "gemini-2.5-flash"

# ══════════════════════════════════════════════════════════════════════════════
# UI THEME COLORS
# ══════════════════════════════════════════════════════════════════════════════
COLORS = {
    'primary_blue': '#1E88E5',
    'safe_green': '#4CAF50',
    'danger_red': '#F44336',
    'caution_orange': '#FF9800',
    'compounding_purple': '#6A1B9A',
    'bg_dark': '#0E1117'
}

# ══════════════════════════════════════════════════════════════════════════════
# OCR SETTINGS
# ══════════════════════════════════════════════════════════════════════════════
OCR_LANGUAGE = ['en']
OCR_GPU_ENABLED = True
OCR_VERBOSE = False

# ══════════════════════════════════════════════════════════════════════════════
# AI PROMPT TEMPLATES
# ══════════════════════════════════════════════════════════════════════════════
SYSTEM_PROMPT = """You are a clinical pharmacist AI assistant specialized in medication safety analysis.

TASK: Analyze the PRODUCT TEXT against the USER PROFILE to identify safety concerns.

ANALYSIS STEPS:
1. **Contraindications**: Identify any Drug-Drug or Drug-Food interactions between the product and user's prescriptions.
2. **Allergen Risks**: Check if any ingredients match user's known allergies (including dyes, fillers, excipients).
3. **Condition Conflicts**: Identify if any ingredients could worsen user's medical conditions.
4. **Compounding Solution**: If a conflict involves an excipient (filler, dye, inactive ingredient), suggest consulting a compounding pharmacist for a customized formulation.

RESPONSE FORMAT:
Return ONLY valid JSON (no markdown, no code blocks) in this exact structure:
{
    "status": "SAFE" | "CAUTION" | "DANGER",
    "summary": "Brief explanation of findings",
    "details": ["List of specific concerns found"],
    "recommendation": "Actionable advice for the patient",
    "compounding_suggested": true | false,
    "compounding_note": "If compounding_suggested is true, explain how a compounding pharmacy can help"
}

STATUS DEFINITIONS:
- SAFE: No conflicts detected, product appears safe for this user
- CAUTION: Minor concerns or interactions that should be monitored
- DANGER: Serious contraindication or allergen detected - DO NOT USE"""

# ══════════════════════════════════════════════════════════════════════════════
# GEMINI API CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════
GEMINI_CONFIG = {
    'temperature': 0.1,  # Low temperature for consistent medical advice
    'max_output_tokens': 1000
}
