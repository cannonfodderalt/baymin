"""
Custom CSS styles for the Contra-Scan application.
"""


def get_custom_css() -> str:
    """
    Return the complete CSS styling for the application.
    
    Returns:
        CSS as a string wrapped in <style> tags
    """
    return """
<style>
    /* Main theme colors */
    :root {
        --primary-blue: #1E88E5;
        --safe-green: #4CAF50;
        --danger-red: #F44336;
        --caution-orange: #FF9800;
        --bg-dark: #0E1117;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #1E3A5F 0%, #2E5077 100%);
        padding: 1.5rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        color: #B0BEC5;
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
    }
    
    /* Status cards */
    .status-card {
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 1rem 0;
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .status-safe {
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
        border: 2px solid #4CAF50;
        box-shadow: 0 0 30px rgba(76, 175, 80, 0.4);
    }
    
    .status-danger {
        background: linear-gradient(135deg, #B71C1C 0%, #C62828 100%);
        border: 2px solid #F44336;
        box-shadow: 0 0 30px rgba(244, 67, 54, 0.4);
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 30px rgba(244, 67, 54, 0.4); }
        50% { box-shadow: 0 0 50px rgba(244, 67, 54, 0.7); }
    }
    
    .status-caution {
        background: linear-gradient(135deg, #E65100 0%, #F57C00 100%);
        border: 2px solid #FF9800;
        box-shadow: 0 0 30px rgba(255, 152, 0, 0.4);
    }
    
    .status-icon {
        font-size: 5rem;
        margin-bottom: 1rem;
    }
    
    .status-text {
        color: white;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    /* Sidebar styling */
    .sidebar-header {
        background: linear-gradient(135deg, #1565C0 0%, #1976D2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .sidebar-header h3 {
        color: white;
        margin: 0;
    }
    
    /* Recommendation box */
    .recommendation-box {
        background: linear-gradient(135deg, #1A237E 0%, #283593 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #7C4DFF;
        margin-top: 1rem;
    }
    
    .recommendation-box h4 {
        color: #B388FF;
        margin: 0 0 0.5rem 0;
    }
    
    .recommendation-box p {
        color: #E8EAF6;
        margin: 0;
        line-height: 1.6;
    }
    
    /* PCCA callout */
    .pcca-callout {
        background: linear-gradient(135deg, #4A148C 0%, #6A1B9A 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #CE93D8;
        margin-top: 1rem;
        text-align: center;
    }
    
    .pcca-callout h4 {
        color: #E1BEE7;
        margin: 0 0 0.5rem 0;
    }
    
    .pcca-callout p {
        color: white;
        margin: 0;
        font-size: 1.1rem;
    }
    
    /* Profile card in sidebar */
    .profile-section {
        background: rgba(30, 136, 229, 0.1);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid rgba(30, 136, 229, 0.3);
        margin-bottom: 1rem;
    }
    
    /* Demo mode banner */
    .demo-banner {
        background: linear-gradient(135deg, #FF6F00 0%, #FF8F00 100%);
        padding: 0.8rem 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .demo-banner p {
        color: white;
        margin: 0;
        font-weight: 600;
    }
    
    /* Scanner area */
    .scanner-area {
        border: 3px dashed #1E88E5;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        background: rgba(30, 136, 229, 0.05);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom button */
    .stButton > button {
        background: linear-gradient(135deg, #1E88E5 0%, #1976D2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(30, 136, 229, 0.4);
    }
</style>
"""
