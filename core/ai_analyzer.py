"""
AI-powered safety analysis using Google Gemini API.
"""

import json
import streamlit as st
from typing import Dict
from config.settings import (
    GEMINI_API_KEY,
    DEMO_MODE,
    GEMINI_MODEL,
    SYSTEM_PROMPT,
    GEMINI_CONFIG
)


def analyze_safety(user_profile: Dict[str, str], scanned_text: str) -> Dict:
    """
    Use Gemini AI to analyze product safety against user's medical profile.
    
    Args:
        user_profile: Dict with prescriptions, allergies, conditions
        scanned_text: OCR-extracted text from product
        
    Returns:
        Analysis result dict with status, summary, recommendation
    """
    
    # ═══════════════════════════════════════════════════════════════════════
    # DEMO MODE - Simulate dangerous interaction for judges
    # ═══════════════════════════════════════════════════════════════════════
    if DEMO_MODE:
        return get_demo_response(user_profile, scanned_text)
    
    # ═══════════════════════════════════════════════════════════════════════
    # LIVE MODE - Call Gemini API
    # ═══════════════════════════════════════════════════════════════════════
    try:
        from google import genai
        
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        # Build user prompt
        user_prompt = _build_user_prompt(user_profile, scanned_text)
        
        # Call Gemini
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=SYSTEM_PROMPT + "\n\n" + user_prompt,
            config=GEMINI_CONFIG
        )
        
        # Parse response
        return _parse_gemini_response(response.text)
        
    except json.JSONDecodeError as e:
        return {
            "status": "CAUTION",
            "summary": "Analysis completed but response parsing failed.",
            "details": [f"Raw response received but couldn't parse: {str(e)}"],
            "recommendation": "Please try scanning again or consult a pharmacist.",
            "compounding_suggested": False,
            "compounding_note": ""
        }
    except Exception as e:
        return {
            "status": "CAUTION",
            "summary": f"Analysis error: {str(e)}",
            "details": ["Could not complete safety analysis"],
            "recommendation": "Please consult a pharmacist directly.",
            "compounding_suggested": False,
            "compounding_note": ""
        }


def _build_user_prompt(user_profile: Dict[str, str], scanned_text: str) -> str:
    """
    Build the user-specific analysis prompt.
    
    Args:
        user_profile: User's medical profile
        scanned_text: Scanned product text
        
    Returns:
        Formatted prompt string
    """
    return f"""
USER PROFILE:
- Current Prescriptions: {user_profile.get('prescriptions', 'None listed')}
- Known Allergies: {user_profile.get('allergies', 'None listed')}
- Medical Conditions: {user_profile.get('conditions', 'None listed')}

PRODUCT TEXT (from label scan):
{scanned_text}

Analyze this product for safety concerns based on the user profile. Return JSON only."""


def _parse_gemini_response(response_text: str) -> Dict:
    """
    Parse and clean Gemini API response.
    
    Args:
        response_text: Raw response from Gemini
        
    Returns:
        Parsed JSON dict
    """
    response_text = response_text.strip()
    
    # Clean up response if it has markdown code blocks
    if "```json" in response_text:
        response_text = response_text.split("```json")[1].split("```")[0]
    elif "```" in response_text:
        response_text = response_text.split("```")[1].split("```")[0]
    
    return json.loads(response_text)


def get_demo_response(user_profile: Dict[str, str], scanned_text: str) -> Dict:
    """
    Generate a demo response showing the PCCA compounding hook.
    Intelligently responds based on user profile and scanned text.
    
    Args:
        user_profile: User's medical profile
        scanned_text: Scanned product text
        
    Returns:
        Simulated analysis result dict
    """
    allergies = user_profile.get('allergies', '').lower()
    prescriptions = user_profile.get('prescriptions', '').lower()
    text_lower = scanned_text.lower()
    
    # Check for dye allergies (PCCA Hook!)
    if 'dye' in allergies or 'red 40' in allergies or 'yellow' in allergies:
        if any(dye in text_lower for dye in ['red 40', 'yellow 5', 'yellow 6', 'blue 1', 'fd&c', 'dye', 'color']):
            return {
                "status": "DANGER",
                "summary": "⚠️ ALLERGEN DETECTED: This product contains artificial dyes that match your allergy profile.",
                "details": [
                    "FD&C Red 40 or similar dye detected in product",
                    "Your profile indicates allergy to: " + user_profile.get('allergies', ''),
                    "Dyes are common excipients in medications and processed foods"
                ],
                "recommendation": "DO NOT USE this product. The artificial coloring could trigger an allergic reaction.",
                "compounding_suggested": True,
                "compounding_note": "💊 A compounding pharmacist can create a DYE-FREE version of this medication using the same active ingredients without artificial colors. PCCA-member pharmacies specialize in these custom formulations."
            }
    
    # Check for Warfarin interactions
    if 'warfarin' in prescriptions:
        if any(word in text_lower for word in ['vitamin k', 'aspirin', 'ibuprofen', 'nsaid', 'ginkgo', 'garlic', 'ginger', 'green tea']):
            return {
                "status": "DANGER",
                "summary": "⚠️ DRUG INTERACTION: This product may dangerously interact with Warfarin.",
                "details": [
                    "Product contains ingredients that affect blood clotting",
                    "Warfarin (blood thinner) detected in your prescriptions",
                    "Combining these could increase bleeding risk or reduce Warfarin effectiveness"
                ],
                "recommendation": "AVOID this product. Consult your doctor or pharmacist before using any supplements while on Warfarin.",
                "compounding_suggested": True,
                "compounding_note": "💊 A compounding pharmacist can formulate alternative supplements that don't interfere with your anticoagulation therapy. Ask about Warfarin-safe vitamin formulations."
            }
    
    # Check for common food allergies
    if any(allergen in allergies for allergen in ['peanut', 'tree nut', 'milk', 'dairy', 'egg', 'wheat', 'gluten', 'soy', 'shellfish']):
        for allergen in ['peanut', 'nut', 'milk', 'dairy', 'egg', 'wheat', 'gluten', 'soy', 'shellfish', 'lactose']:
            if allergen in text_lower:
                return {
                    "status": "DANGER",
                    "summary": f"⚠️ ALLERGEN DETECTED: This product contains {allergen} which is in your allergy list.",
                    "details": [
                        f"'{allergen}' found in product ingredients",
                        f"Your allergy profile includes: {user_profile.get('allergies', '')}",
                        "Cross-contamination may also be a concern"
                    ],
                    "recommendation": f"DO NOT CONSUME. This product contains or may contain {allergen}.",
                    "compounding_suggested": False,
                    "compounding_note": ""
                }
    
    # Check for hypertension concerns
    if 'hypertension' in user_profile.get('conditions', '').lower():
        if any(word in text_lower for word in ['sodium', 'salt', 'caffeine', 'pseudoephedrine', 'decongestant']):
            return {
                "status": "CAUTION",
                "summary": "⚠️ CONDITION CONCERN: This product may not be ideal for your blood pressure condition.",
                "details": [
                    "High sodium/stimulant content detected",
                    "Your profile indicates Hypertension",
                    "This could potentially raise blood pressure"
                ],
                "recommendation": "Use with caution. Consider low-sodium alternatives or consult your doctor.",
                "compounding_suggested": True,
                "compounding_note": "💊 Compounding pharmacies can create sodium-free or stimulant-free versions of many medications for patients with hypertension."
            }
    
    # Default safe response
    return {
        "status": "SAFE",
        "summary": "✅ No conflicts detected between this product and your medical profile.",
        "details": [
            "No known allergens matching your profile",
            "No significant drug interactions identified",
            "Product appears compatible with your conditions"
        ],
        "recommendation": "This product appears safe based on your profile. Always read the full label and consult a pharmacist if unsure.",
        "compounding_suggested": False,
        "compounding_note": ""
    }
