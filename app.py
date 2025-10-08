import streamlit as st
import requests
import time
import os
import json
import sys
from datetime import datetime
from pathlib import Path
from PIL import Image
import io

# Page configuration
st.set_page_config(
    page_title="Sora Video Generator",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Modern, responsive CSS with dark mode support
st.markdown("""
    <style>
    /* CSS Variables for theming */
    :root {
        --bg-primary: #ffffff;
        --bg-secondary: #f8fafc;
        --bg-tertiary: #f1f5f9;
        --text-primary: #0f172a;
        --text-secondary: #334155;
        --text-muted: #64748b;
        --border-color: #e2e8f0;
        --border-focus: #94a3b8;
        --accent-primary: #0f172a;
        --accent-hover: #1e293b;
        --success-bg: #f0fdf4;
        --success-border: #86efac;
        --success-text: #166534;
        --shadow-focus: rgba(148, 163, 184, 0.1);
    }
    
    /* Dark mode variables */
    @media (prefers-color-scheme: dark) {
        :root {
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --bg-tertiary: #334155;
            --text-primary: #f8fafc;
            --text-secondary: #e2e8f0;
            --text-muted: #94a3b8;
            --border-color: #475569;
            --border-focus: #64748b;
            --accent-primary: #3b82f6;
            --accent-hover: #2563eb;
            --success-bg: #064e3b;
            --success-border: #10b981;
            --success-text: #34d399;
            --shadow-focus: rgba(59, 130, 246, 0.1);
        }
    }
    
    /* Base responsive container */
    .main {
        padding: 1rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    @media (min-width: 640px) {
        .main {
            padding: 1.5rem;
        }
    }
    
    @media (min-width: 768px) {
        .main {
            padding: 2rem;
        }
    }
    
    @media (min-width: 1024px) {
        .main {
            padding: 3rem;
        }
    }
    
    /* Typography - responsive */
    h1 {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        color: var(--text-primary) !important;
        margin-bottom: 0.5rem !important;
    }
    
    @media (min-width: 640px) {
        h1 {
            font-size: 2rem !important;
        }
    }
    
    h2 {
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: var(--text-secondary) !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    @media (min-width: 640px) {
        h2 {
            font-size: 1.125rem !important;
            margin-top: 2rem !important;
        }
    }
    
    /* Generate button - responsive */
    .stButton>button {
        width: 100%;
        background-color: var(--accent-primary);
        color: white;
        font-size: 16px;
        font-weight: 500;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        border: none;
        transition: all 0.15s ease;
        margin: 1.5rem 0 1rem 0;
    }
    
    @media (min-width: 640px) {
        .stButton>button {
            padding: 0.875rem 1.5rem;
        margin: 2rem 0 1rem 0;
        }
    }
    
    .stButton>button:hover {
        background-color: var(--accent-hover);
        transform: translateY(-1px);
    }
    
    /* Text area - responsive */
    .stTextArea textarea {
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        font-size: 14px !important;
        line-height: 1.6 !important;
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }
    
    @media (min-width: 640px) {
        .stTextArea textarea {
        padding: 1rem !important;
        font-size: 15px !important;
        }
    }
    
    .stTextArea textarea:focus {
        border-color: var(--border-focus) !important;
        box-shadow: 0 0 0 3px var(--shadow-focus) !important;
    }
    
    /* Settings boxes - responsive */
    .info-box {
        padding: 1rem;
        border-radius: 8px;
        background-color: var(--bg-secondary);
        border: 1px solid var(--border-color);
        margin: 0;
        color: var(--text-secondary);
        font-size: 13px;
        line-height: 1.6;
        word-break: break-word;
    }
    
    @media (min-width: 640px) {
        .info-box {
            padding: 1.25rem;
        font-size: 14px;
        line-height: 1.8;
        }
    }
    
    .info-box strong {
        color: var(--text-muted);
        font-weight: 500;
        font-size: 12px;
    }
    
    @media (min-width: 640px) {
        .info-box strong {
        font-size: 13px;
        }
    }
    
    /* Cost display - responsive */
    .cost-box {
        padding: 1rem;
        border-radius: 8px;
        background-color: var(--success-bg);
        border: 1px solid var(--success-border);
        margin: 0;
        color: var(--success-text);
        font-size: 13px;
        line-height: 1.6;
        text-align: center;
    }
    
    @media (min-width: 640px) {
        .cost-box {
            padding: 1.25rem;
        font-size: 14px;
        line-height: 1.8;
        }
    }
    
    .cost-box strong {
        font-weight: 600;
        font-size: 16px;
    }
    
    @media (min-width: 640px) {
        .cost-box strong {
        font-size: 18px;
        }
    }
    
    /* Video display - responsive */
    video {
        max-width: 100%;
        height: auto;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    @media (min-width: 640px) {
        video {
        margin: 1.5rem 0;
        }
    }
    
    /* Sidebar styling - responsive */
    section[data-testid="stSidebar"] {
        background-color: var(--bg-secondary);
        border-right: 1px solid var(--border-color);
    }
    
    section[data-testid="stSidebar"] .stSelectbox,
    section[data-testid="stSidebar"] .stTextInput {
        margin-bottom: 0.5rem;
    }
    
    @media (min-width: 640px) {
        section[data-testid="stSidebar"] .stSelectbox,
        section[data-testid="stSidebar"] .stTextInput {
            margin-bottom: 0.75rem;
        }
    }
    
    /* Mobile sidebar improvements */
    @media (max-width: 767px) {
        section[data-testid="stSidebar"] {
            padding: 0.5rem;
        }
        
        section[data-testid="stSidebar"] .stSelectbox,
        section[data-testid="stSidebar"] .stTextInput {
            margin-bottom: 0.5rem;
        }
        
        /* Hide sidebar on mobile by default */
        .css-1d391kg {
            display: none;
        }
        
        /* Show toggle button */
        .css-1v0mbdj {
            display: block !important;
        }
    }
    
    /* Clean dividers */
    hr {
        margin: 1.5rem 0;
        border: none;
        height: 1px;
        background-color: var(--border-color);
    }
    
    @media (min-width: 640px) {
        hr {
            margin: 2.5rem 0;
        }
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-size: 13px;
        font-weight: 500;
        color: var(--text-muted);
    }
    
    @media (min-width: 640px) {
        .streamlit-expanderHeader {
            font-size: 14px;
        }
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
    }
    
    @media (min-width: 640px) {
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        }
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 6px 12px;
        font-size: 13px;
        font-weight: 500;
        color: var(--text-muted);
    }
    
    @media (min-width: 640px) {
    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        font-size: 14px;
        }
    }
    
    .stTabs [aria-selected="true"] {
        color: var(--text-primary);
    }
    
    /* Progress indicators */
    .stProgress > div > div {
        background-color: var(--accent-primary);
    }
    
    /* Clean alerts */
    .stAlert {
        padding: 10px 12px;
        border-radius: 6px;
        font-size: 13px;
    }
    
    @media (min-width: 640px) {
        .stAlert {
            padding: 12px 16px;
        font-size: 14px;
        }
    }
    
    /* Responsive columns */
    .stColumns > div {
        padding: 0.25rem;
    }
    
    @media (min-width: 640px) {
        .stColumns > div {
            padding: 0.5rem;
        }
    }
    
    /* Mobile-first spacing */
    .block-container {
        padding-top: 0.5rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    
    @media (min-width: 640px) {
        .block-container {
            padding-top: 1.5rem;
            padding-left: 1.5rem;
            padding-right: 1.5rem;
        }
    }
    
    @media (min-width: 768px) {
    .block-container {
        padding-top: 2rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }
    }
    
    /* Input styling for dark mode */
    .stTextInput input,
    .stSelectbox select,
    .stTextArea textarea {
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        border-color: var(--border-color) !important;
    }
    
    .stTextInput input:focus,
    .stSelectbox select:focus,
    .stTextArea textarea:focus {
        border-color: var(--border-focus) !important;
        box-shadow: 0 0 0 3px var(--shadow-focus) !important;
    }
    
    /* Caption styling */
    .stCaption {
        color: var(--text-muted) !important;
        font-size: 12px !important;
    }
    
    @media (min-width: 640px) {
        .stCaption {
            font-size: 13px !important;
        }
    }
    
    /* Mobile navigation improvements */
    @media (max-width: 767px) {
        /* Make sure main content doesn't get cut off */
        .main .block-container {
            padding-left: 0.75rem !important;
            padding-right: 0.75rem !important;
            padding-top: 3.5rem !important;
        }
        
        /* Better spacing for main title */
        h1 {
            margin-top: 1.5rem !important;
            margin-bottom: 0.25rem !important;
        }
        
        /* Reduce spacing between title and caption */
        .stCaption {
            margin-bottom: 1.5rem !important;
        }
        
        /* Better button spacing on mobile */
        .stButton {
            margin: 1.5rem 0 !important;
        }
        
        /* Compact settings summary on mobile */
        .info-box {
            font-size: 12px !important;
            padding: 0.75rem !important;
            margin: 0.5rem 0 !important;
        }
        
        .cost-box {
            font-size: 12px !important;
            padding: 0.75rem !important;
            margin: 0.5rem 0 !important;
        }
        
        .cost-box strong {
            font-size: 14px !important;
        }
        
        /* Better spacing for text area */
        .stTextArea {
            margin: 1rem 0 !important;
        }
        
        /* Better spacing for expander */
        .streamlit-expander {
            margin: 0.75rem 0 !important;
        }
        
        /* Reduce spacing between columns */
        .stColumns > div {
            padding: 0.125rem !important;
        }
        
        /* Better spacing for video history */
        .stTabs {
            margin-top: 2rem !important;
        }
    }
    
    /* Progress section animations */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Animate progress sections */
    .progress-section {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Video responsiveness */
    video {
        max-width: 100%;
        height: auto;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Ensure video container is responsive */
    .stVideo {
        width: 100% !important;
    }
    
    /* Download button styling */
    .stDownloadButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 1.5rem !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        transition: all 0.15s ease !important;
        margin-top: 0.5rem !important;
    }
    
    .stDownloadButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Dark mode specific overrides */
    @media (prefers-color-scheme: dark) {
        /* Ensure Streamlit components respect dark mode */
        .stApp {
            background-color: var(--bg-primary) !important;
        }
        
        /* Fix any remaining light mode elements */
        .stMarkdown {
            color: var(--text-primary) !important;
        }
        
        /* Better contrast for dark mode */
        .stExpander .streamlit-expanderContent {
            background-color: var(--bg-secondary) !important;
            border: 1px solid var(--border-color) !important;
        }
        
        video {
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
    }
    
    /* Mobile optimizations */
    @media (max-width: 768px) {
        video {
            border-radius: 4px;
        }
        
        .stDownloadButton>button {
            font-size: 14px !important;
            padding: 0.625rem 1rem !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

def resize_image_to_dimensions(image_file, target_width, target_height):
    """Resize an image to match the target dimensions
    
    Args:
        image_file: Uploaded file object
        target_width: Target width in pixels
        target_height: Target height in pixels
    
    Returns:
        BytesIO object containing resized image, or None if error
    """
    try:
        # Read the image
        img = Image.open(image_file)
        
        # Get current dimensions
        current_width, current_height = img.size
        
        # If already correct size, return original
        if current_width == target_width and current_height == target_height:
            image_file.seek(0)  # Reset file pointer
            return image_file
        
        # Resize the image
        resized_img = img.resize((target_width, target_height), Image.LANCZOS)
        
        # Save to BytesIO
        output = io.BytesIO()
        # Preserve format or default to PNG
        img_format = img.format if img.format else 'PNG'
        resized_img.save(output, format=img_format)
        output.seek(0)
        
        # Set the name attribute to match original file
        output.name = getattr(image_file, 'name', 'resized_image.png')
        
        return output
    except Exception as e:
        st.error(f"Error resizing image: {str(e)}")
        return None

def calculate_cost(model, resolution, duration):
    """Calculate estimated cost based on model, resolution, and duration"""
    # Pricing per second (approximate based on available data)
    # Note: These are estimates - check OpenAI's official pricing
    pricing = {
        'sora-2-pro': {
            '720p': 0.30,    # 1280x720 and 720x1280
            '1080p': 0.50,   # 1792x1024 and 1024x1792
        },
        'sora-2': {
            '720p': 0.10,    # 1280x720 and 720x1280
            '1080p': 0.10,   # Same price for both resolutions
        }
    }
    
    # Determine resolution tier based on dimensions
    if '1792' in resolution or '1024' in resolution:
        tier = '1080p'
    elif '1280' in resolution or '720' in resolution:
        tier = '720p'
    else:
        tier = '720p'
    
    cost_per_second = pricing.get(model, {}).get(tier, 0.20)
    total_cost = cost_per_second * duration
    
    return total_cost, cost_per_second

def create_video(api_key, prompt, size, duration, model='sora-2-pro', input_reference=None):
    """Create a video using the Sora API
    
    Args:
        api_key: OpenAI API key
        prompt: Text description of the video
        size: Video resolution (e.g., '1280x720')
        duration: Video duration in seconds
        model: Model to use (default: 'sora-2-pro')
        input_reference: Optional image or video file for guided generation
    """
    headers = {
        'Authorization': f'Bearer {api_key}',
    }
    
    # Use multipart/form-data if input_reference is provided, otherwise JSON
    if input_reference is not None:
        # Multipart form data for image/video upload
        files = {
            'input_reference': input_reference
        }
        data = {
            'model': model,
            'prompt': prompt,
            'size': size,
            'seconds': str(duration)
        }
        
        try:
            response = requests.post(
                'https://api.openai.com/v1/videos',
                headers=headers,
                data=data,
                files=files,
                timeout=30
            )
        except Exception as e:
            st.error(f"Error uploading input reference: {str(e)}")
            return None
    else:
        # JSON request for text-to-video
        headers['Content-Type'] = 'application/json'
        data = {
            'model': model,
            'prompt': prompt,
            'size': size,
            'seconds': str(duration)
        }
        
        try:
            response = requests.post(
                'https://api.openai.com/v1/videos',
                headers=headers,
                json=data,
                timeout=30
            )
        except requests.exceptions.Timeout:
            st.error("⏰ Request timed out. Please try again.")
            return None
        except requests.exceptions.RequestException as e:
            st.error(f"🌐 Network error: {str(e)}")
            return None
        except Exception as e:
            st.error(f"💥 Unexpected error: {str(e)}")
            return None
    
    # Handle response (common for both JSON and multipart)
    try:
        if response.status_code in [200, 202]:
            response_data = response.json()
            return response_data
        else:
            st.error(f"❌ API Error: {response.status_code}")
            try:
                error_response = response.json()
                if 'error' in error_response:
                    error_details = error_response['error']
                    st.error(f"Error: {error_details.get('message', 'Unknown error')}")
            except:
                st.error(f"Response: {response.text}")
            
            return None
    except Exception as e:
        st.error(f"💥 Error processing response: {str(e)}")
        return None

def check_video_status(api_key, video_id):
    """Check the status of a video generation"""
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    
    try:
        response = requests.get(
            f'https://api.openai.com/v1/videos/{video_id}',
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
            
    except Exception as e:
        st.error(f"Error checking status: {str(e)}")
        return None

def get_video_content_url(api_key, video_id):
    """Get the video content URL for streaming/downloading"""
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    
    try:
        response = requests.get(
            f'https://api.openai.com/v1/videos/{video_id}/content',
            headers=headers,
            timeout=30,
            stream=True
        )
        
        if response.status_code == 200:
            # The content endpoint streams the video, so we need to handle it differently
            # For Streamlit, we can't directly stream, but we can save it temporarily
            import tempfile
            import os
            
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        tmp_file.write(chunk)
                temp_path = tmp_file.name
            
            # Return the path to the temporary file
            return temp_path
        else:
            st.error(f"Error getting video content: {response.status_code}")
            return None
            
    except Exception as e:
        st.error(f"Error getting video content: {str(e)}")
        return None

def main():
    # Clean header
    st.title("Sora Video Generator")
    st.caption("AI video generation powered by OpenAI")
    
    # Initialize session state for generation tracking
    if 'generation_in_progress' not in st.session_state:
        st.session_state.generation_in_progress = False
    if 'current_video_id' not in st.session_state:
        st.session_state.current_video_id = None
    if 'generation_start_time' not in st.session_state:
        st.session_state.generation_start_time = None
    if 'generation_settings' not in st.session_state:
        st.session_state.generation_settings = {}
    if 'status_check_fails' not in st.session_state:
        st.session_state.status_check_fails = 0
    if 'last_known_status' not in st.session_state:
        st.session_state.last_known_status = None
    
    # Sidebar for configuration
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)
        
        # API Key input
        api_key = st.text_input(
            "🔑 API Key",
            type="password",
            value=os.environ.get("OPENAI_API_KEY", ""),
            placeholder="sk-...",
            help="Enter your OpenAI API key"
        )
        
        if not api_key:
            st.caption("⚠️ API key required")
        
        st.markdown("<div style='margin: 1rem 0 0.5rem 0;'></div>", unsafe_allow_html=True)
        
        # Model selection
        st.markdown("**🤖 Model**")
        
        model = st.selectbox(
            "Choose Model",
            options=[
                "sora-2-pro",
                "sora-2"
            ],
            label_visibility="collapsed",
            help="Select the AI model for video generation"
        )
        
        # Model descriptions
        model_info = {
            "sora-2-pro": "Highest quality with audio",
            "sora-2": "Balanced quality & speed"
        }
        
        st.caption(model_info[model])
        
        st.markdown("<div style='margin: 1rem 0 0.5rem 0;'></div>", unsafe_allow_html=True)
        
        # Video settings
        st.markdown("**🎥 Video Settings**")
        
        # Resolution selector - API only supports specific values
        # Show different options based on selected model
        if model == "sora-2":
            resolution_options = [
                "1280x720",   # 16:9 HD
                "720x1280",   # 9:16 HD
            ]
        else:  # sora-2-pro
            resolution_options = [
                "1280x720",   # 16:9 HD
                "720x1280",   # 9:16 HD  
                "1792x1024",  # 16:9 Full HD
                "1024x1792",  # 9:16 Full HD
            ]
        
        size = st.selectbox(
            "📐 Resolution",
            options=resolution_options,
            help=f"Choose video resolution ({'720p only for sora-2' if model == 'sora-2' else '720p and 1080p available'})"
        )
        
        # Map resolution to display names
        resolution_names = {
            "1280x720": "16:9 HD (1280×720)",
            "720x1280": "9:16 HD (720×1280)", 
            "1792x1024": "16:9 Full HD (1792×1024)",
            "1024x1792": "9:16 Full HD (1024×1792)"
        }
        
        st.caption(resolution_names[size])
        
        # Duration selector - API only accepts 4, 8, or 12 seconds
        duration_options = {
            "4 seconds": 4,
            "8 seconds": 8,
            "12 seconds": 12
        }
        
        duration_label = st.selectbox(
            "⏱️ Duration",
            options=list(duration_options.keys()),
            index=0,
            help="Video length - API supports 4, 8, or 12 seconds"
        )
        
        duration = duration_options[duration_label]
    
    # Main content
    st.markdown("#")  # Reduced spacing
    
    # Prompt input - main focus
    prompt = st.text_area(
        "🎬 Video Description",
        height=120,
        placeholder="Describe the video you want to generate...\n\nExample: A serene sunrise over a misty mountain lake, with a lone canoe gliding across the water. The camera slowly pans from left to right.",
        label_visibility="collapsed",
        help="Be descriptive and specific about what you want to see in your video"
    )
    
    # Input reference upload (optional)
    st.markdown("<div style='margin: 1rem 0 0.5rem 0;'></div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "🖼️ Input Reference (Optional)",
        type=['png', 'jpg', 'jpeg', 'webp', 'mp4', 'mov', 'avi'],
        help="Upload an image or video to guide the generation. Sora will animate/transform it based on your prompt.",
        label_visibility="visible"
    )
    
    # Show preview if file uploaded
    if uploaded_file is not None:
        file_type = uploaded_file.type
        col_preview1, col_preview2, col_preview3 = st.columns([1, 2, 1])
        with col_preview2:
            if file_type.startswith('image'):
                st.image(uploaded_file, caption="Input Image", use_container_width=True)
                
                # Check image dimensions
                try:
                    uploaded_file.seek(0)  # Reset file pointer
                    img = Image.open(uploaded_file)
                    img_width, img_height = img.size
                    uploaded_file.seek(0)  # Reset again for later use
                    
                    # Parse target dimensions
                    target_width, target_height = map(int, size.split('x'))
                    
                    if img_width == target_width and img_height == target_height:
                        st.caption(f"✅ Perfect! Image is {img_width}x{img_height} (matches selected resolution)")
                    else:
                        st.warning(f"📐 Image is {img_width}x{img_height} but selected resolution is {size}")
                        st.caption("✨ Don't worry - image will be automatically resized to match!")
                except Exception as e:
                    st.caption("✅ Image uploaded - Sora will animate this based on your prompt")
                    
            elif file_type.startswith('video'):
                st.video(uploaded_file)
                st.caption("✅ Video uploaded - Sora will transform this based on your prompt")
        
        st.info("⚠️ **Note:** Uploading images depicting real people is restricted. Use your own likeness only with explicit permission.")
    
    # Example prompts - collapsible and mobile-friendly
    with st.expander("💡 Example prompts"):
        st.markdown("**Text-to-Video (No input reference):**")
        st.markdown("**Nature & Landscapes:**")
        st.code("A majestic waterfall cascading down moss-covered rocks in a lush rainforest, sunlight filtering through the canopy", language=None)
        
        st.markdown("**Urban & City:**")
        st.code("A bustling Tokyo street at night, neon signs reflecting on wet pavement after rain, camera tracking shot", language=None)
        
        st.markdown("**Space & Sci-Fi:**")
        st.code("An astronaut floating in space, Earth visible in the background, dramatic lighting from the sun, wide cinematic shot", language=None)
        
        st.markdown("---")
        st.markdown("**Image-to-Video (With input reference):**")
        st.markdown("**Animate a Photo:**")
        st.code("The person smiles and waves at the camera, their hair gently blowing in the breeze", language=None)
        
        st.markdown("**Transform a Scene:**")
        st.code("The camera slowly zooms into the building, clouds moving across the sky, birds flying past", language=None)
        
        st.markdown("**Add Motion:**")
        st.code("The waves crash against the shore, the sun setting creates a golden glow across the water", language=None)
    
    # Settings summary - responsive layout
    st.markdown("<div style='margin: 1rem 0 0.75rem 0;'></div>", unsafe_allow_html=True)
    
    # Calculate cost for display
    total_cost, cost_per_sec = calculate_cost(model, size, duration)
    
    # Use responsive columns that stack on mobile
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"""
        <div class="info-box">
        <strong>MODEL:</strong> {model} &nbsp;•&nbsp; <strong>RESOLUTION:</strong> {resolution_names[size]} &nbsp;•&nbsp; <strong>DURATION:</strong> {duration}s
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="cost-box">
        <strong>${total_cost:.2f}</strong><br>
        <small>estimated</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Show warning if generation is in progress
    if st.session_state.generation_in_progress:
        st.warning("🔄 Video generation is currently in progress. Please wait for it to complete before starting a new generation.")
        
        # Show current generation info
        if st.session_state.current_video_id:
            st.info(f"📹 Current Video ID: `{st.session_state.current_video_id}`")
        
        # Add stop generation button
        if st.button("🛑 Stop Current Generation", type="secondary"):
            st.session_state.generation_in_progress = False
            st.session_state.current_video_id = None
            st.session_state.generation_start_time = None
            st.session_state.generation_settings = {}
            st.session_state.status_check_fails = 0
            st.session_state.last_known_status = None
            st.success("✅ Generation stopped")
            st.rerun()
        
        # Resume progress tracking for ongoing generation
        if st.session_state.current_video_id and st.session_state.generation_settings:
            settings = st.session_state.generation_settings
            video_id = st.session_state.current_video_id
            
            # Get settings from session state
            api_key = settings.get('api_key')
            model = settings.get('model')
            
            # Estimated time based on model
            estimated_times = {
                'sora-2-pro': (60, 120),  # 1-2 minutes
                'sora-2': (45, 90),       # 45s-1.5min
            }
            est_min, est_max = estimated_times.get(model, (45, 90))
            
            # Enhanced progress section
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 1.5rem;
                border-radius: 12px;
                color: white;
                margin: 1rem 0;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            ">
                <h4 style="margin: 0 0 1rem 0; color: white;">🎬 Video Generation Progress</h4>
                <p style="margin: 0 0 1rem 0; opacity: 0.9;">⏱️ Estimated time: <strong>{est_min}-{est_max} seconds</strong> (varies by complexity)</p>
            </div>
            """.format(est_min=est_min, est_max=est_max), unsafe_allow_html=True)
            
            # Progress indicators with better styling
            progress_bar = st.progress(0)
            
            # Status display columns
            col_status, col_time = st.columns([1, 1])
            
            with col_status:
                api_status_text = st.empty()
            
            with col_time:
                status_text = st.empty()
            
            # Check status once (no loop for resumed sessions)
            start_time = st.session_state.generation_start_time or time.time()
            elapsed = int(time.time() - start_time)
            
            # Simulated progress based on elapsed time vs estimated time
            progress = min((elapsed / est_max) * 90, 95)
            progress_bar.progress(int(progress))
            
            # Enhanced status display
            status_text.markdown(f"""
            <div style="
                background-color: var(--bg-secondary);
                padding: 0.75rem;
                border-radius: 8px;
                border-left: 4px solid #3b82f6;
                margin: 0.5rem 0;
            ">
                <strong>⏳ Elapsed:</strong> {elapsed}s
            </div>
            """, unsafe_allow_html=True)
            
            # Check current video status
            video_status = check_video_status(api_key, video_id)
            
            status_emojis = {
                'processing': '🔄',
                'in_progress': '🔄',
                'queued': '⏸️',
                'succeeded': '✅',
                'completed': '✅',
                'failed': '❌'
            }
            status_colors = {
                'processing': '#f59e0b',
                'in_progress': '#3b82f6',
                'queued': '#6b7280',
                'succeeded': '#10b981',
                'completed': '#10b981',
                'failed': '#ef4444'
            }
            
            if video_status and isinstance(video_status, dict):
                status = video_status.get('status')
                st.session_state.status_check_fails = 0
                
                if status:
                    st.session_state.last_known_status = status
                
                emoji = status_emojis.get(status, '⏳')
                color = status_colors.get(status, '#6b7280')
                
                api_status_text.markdown(f"""
                <div style="
                    background-color: var(--bg-secondary);
                    padding: 0.75rem;
                    border-radius: 8px;
                    border-left: 4px solid {color};
                    margin: 0.5rem 0;
                ">
                    <strong>{emoji} Status:</strong> {status.title()}
                </div>
                """, unsafe_allow_html=True)
                
                if status in ['succeeded', 'completed']:
                    progress_bar.progress(100)
                    
                    # Enhanced completion message
                    status_text.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                        padding: 1rem;
                        border-radius: 8px;
                        color: white;
                        margin: 0.5rem 0;
                        text-align: center;
                        animation: pulse 2s infinite;
                    ">
                        <strong>🎉 Video Ready!</strong>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Get the video content using the correct API endpoint
                    st.info("🔄 Fetching video content...")
                    video_content_path = get_video_content_url(api_key, video_id)
                    
                    if video_content_path:
                        st.success("✅ Video content downloaded successfully!")
                        video_url = video_content_path  # Use the local file path for Streamlit
                    else:
                        st.error("❌ Failed to download video content")
                        video_url = None
                    
                    if video_url:
                        st.balloons()
                        
                        # Enhanced video display section - responsive
                        st.markdown("""
                        <div style="
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            padding: 1.5rem;
                            border-radius: 12px;
                            color: white;
                            margin: 1rem 0;
                            text-align: center;
                        ">
                            <h3 style="margin: 0; color: white;">🎬 Your Generated Video</h3>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Responsive video container
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                            st.video(video_url)
                        
                        st.success("✅ Video displayed successfully!")
                        
                        # Download button
                        with open(video_url, 'rb') as video_file:
                            video_bytes = video_file.read()
                            st.download_button(
                                label="⬇️ Download Video",
                                data=video_bytes,
                                file_name=f"sora_video_{video_id}.mp4",
                                mime="video/mp4",
                                use_container_width=True
                            )
                        
                        # Save to session history
                        if 'video_history' not in st.session_state:
                            st.session_state.video_history = []
                        
                        st.session_state.video_history.insert(0, {
                            'prompt': settings.get('prompt'),
                            'url': video_url,
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'model': model,
                            'size': settings.get('size'),
                            'duration': settings.get('duration'),
                            'video_id': video_id,
                            'status': 'completed'
                        })
                    
                    # Clear generation state when completed
                    st.session_state.generation_in_progress = False
                    st.session_state.current_video_id = None
                    st.session_state.generation_start_time = None
                    st.session_state.generation_settings = {}
                    st.session_state.status_check_fails = 0
                    st.session_state.last_known_status = None
                    
                elif status == 'failed':
                    error_msg = video_status.get('error', 'Unknown error')
                    st.error(f"❌ Video generation failed: {error_msg}")
                    
                    # Clear generation state when failed
                    st.session_state.generation_in_progress = False
                    st.session_state.current_video_id = None
                    st.session_state.generation_start_time = None
                    st.session_state.generation_settings = {}
                    st.session_state.status_check_fails = 0
                    st.session_state.last_known_status = None
                else:
                    # Generation is still in progress - will auto-refresh at end of page
                    pass
            else:
                # video_status is None or not a dict
                # Increment fail counter
                st.session_state.status_check_fails += 1
                
                # Max retries before assuming content violation or error
                MAX_RETRIES = 10  # 30 seconds of retries
                
                # If we had a valid status before (in_progress/queued) but now getting None,
                # and we've exceeded max retries, assume content violation or error
                if (st.session_state.last_known_status in ['processing', 'in_progress', 'queued'] 
                    and st.session_state.status_check_fails >= MAX_RETRIES):
                    
                    api_status_text.markdown("""
                    <div style="
                        background-color: var(--bg-secondary);
                        padding: 0.75rem;
                        border-radius: 8px;
                        border-left: 4px solid #ef4444;
                        margin: 0.5rem 0;
                    ">
                        <strong>❌ Status:</strong> Likely Failed
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.error("""
                    ❌ **Video generation likely failed**
                    
                    The video was processing but the API is no longer returning status information. 
                    This typically happens when:
                    - Content policy violation detected
                    - Generation failed due to an error
                    - Video ID is invalid or expired
                    
                    Please try generating a new video with a different prompt.
                    """)
                    
                    # Clear generation state
                    st.session_state.generation_in_progress = False
                    st.session_state.current_video_id = None
                    st.session_state.generation_start_time = None
                    st.session_state.generation_settings = {}
                    st.session_state.status_check_fails = 0
                    st.session_state.last_known_status = None
                    
                    st.stop()
                    
                elif st.session_state.status_check_fails >= MAX_RETRIES:
                    # Too many fails even without prior status
                    api_status_text.markdown("""
                    <div style="
                        background-color: var(--bg-secondary);
                        padding: 0.75rem;
                        border-radius: 8px;
                        border-left: 4px solid #ef4444;
                        margin: 0.5rem 0;
                    ">
                        <strong>❌ Status:</strong> Check Failed
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.error("❌ Unable to check video status after multiple attempts. Please try again or check your API key.")
                    
                    # Clear generation state
                    st.session_state.generation_in_progress = False
                    st.session_state.current_video_id = None
                    st.session_state.generation_start_time = None
                    st.session_state.generation_settings = {}
                    st.session_state.status_check_fails = 0
                    st.session_state.last_known_status = None
                    
                    st.stop()
                    
                else:
                    # Still retrying
                    api_status_text.markdown(f"""
                    <div style="
                        background-color: var(--bg-secondary);
                        padding: 0.75rem;
                        border-radius: 8px;
                        border-left: 4px solid #6b7280;
                        margin: 0.5rem 0;
                    ">
                        <strong>⏳ Status:</strong> Checking... (Attempt {st.session_state.status_check_fails}/{MAX_RETRIES})
                    </div>
                    """, unsafe_allow_html=True)
    
    # Generate button (only show if not currently generating)
    if not st.session_state.generation_in_progress:
        generate_button = st.button(
            "🎬 Generate Video", 
            disabled=not api_key or not prompt, 
            use_container_width=True, 
            type="primary"
        )
    else:
        generate_button = False
    
    if generate_button:
        if not api_key:
            st.error("❌ Please enter your OpenAI API key in the sidebar")
        elif not prompt:
            st.error("❌ Please enter a prompt")
        else:
            # Set generation in progress
            st.session_state.generation_in_progress = True
            st.session_state.generation_start_time = time.time()
            st.session_state.generation_settings = {
                'api_key': api_key,
                'prompt': prompt,
                'size': size,
                'duration': duration,
                'model': model
            }
            # Reset status check counters for new generation
            st.session_state.status_check_fails = 0
            st.session_state.last_known_status = None
            
            # Create video
            input_ref_message = " with input reference" if uploaded_file else ""
            
            # Prepare input reference (resize image if needed)
            prepared_input = None
            if uploaded_file is not None:
                file_type = uploaded_file.type
                if file_type.startswith('image'):
                    # Parse target dimensions
                    target_width, target_height = map(int, size.split('x'))
                    
                    # Resize image to match target dimensions
                    with st.spinner(f"📐 Preparing image ({size})..."):
                        prepared_input = resize_image_to_dimensions(uploaded_file, target_width, target_height)
                    
                    if prepared_input is None:
                        st.error("❌ Failed to prepare image. Please try a different image.")
                        st.session_state.generation_in_progress = False
                        st.session_state.status_check_fails = 0
                        st.session_state.last_known_status = None
                        st.stop()
                    
                    st.success(f"✅ Image prepared: {target_width}x{target_height}")
                else:
                    # For videos, use as-is (API may have different requirements)
                    prepared_input = uploaded_file
            
            with st.spinner(f"🎨 Creating your video with {model}{input_ref_message}..."):
                result = create_video(api_key, prompt, size, duration, model, input_reference=prepared_input)
                
                if result and isinstance(result, dict):
                    video_id = result.get('id')
                    if not video_id:
                        st.error("❌ Video creation failed: No video ID returned")
                        st.session_state.generation_in_progress = False
                        st.session_state.status_check_fails = 0
                        st.session_state.last_known_status = None
                    else:
                        st.session_state.current_video_id = video_id
                    st.success(f"✅ Video creation started! ID: {video_id}")
                    
                    # Note: OpenAI's API only returns status states (processing/succeeded/failed),
                    # not granular progress percentages. We show elapsed time and estimated completion.
                    
                    # Estimated time based on model
                    estimated_times = {
                        'sora-2-pro': (60, 120),  # 1-2 minutes
                        'sora-2': (45, 90),       # 45s-1.5min
                    }
                    est_min, est_max = estimated_times.get(model, (45, 90))
                    
                    # Enhanced progress section
                    st.markdown("""
                        <div style="
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            padding: 1.5rem;
                            border-radius: 12px;
                            color: white;
                            margin: 1rem 0;
                            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        ">
                            <h4 style="margin: 0 0 1rem 0; color: white;">🎬 Video Generation Progress</h4>
                            <p style="margin: 0 0 1rem 0; opacity: 0.9;">⏱️ Estimated time: <strong>{est_min}-{est_max} seconds</strong> (varies by complexity)</p>
                        </div>
                        """.format(est_min=est_min, est_max=est_max), unsafe_allow_html=True)
                    
                    # Progress indicators with better styling
                    progress_container = st.container()
                    with progress_container:
                        progress_bar = st.progress(0)
                        
                        # Status display columns
                        col_status, col_time = st.columns([1, 1])
                        
                        with col_status:
                            api_status_text = st.empty()
                        
                        with col_time:
                            status_text = st.empty()
                    
                    # Check video status (will auto-refresh via JavaScript)
                    start_time = st.session_state.generation_start_time or time.time()
                    elapsed = int(time.time() - start_time)
                    
                    # Simulated progress based on elapsed time vs estimated time
                    progress = min((elapsed / est_max) * 90, 95)
                    progress_bar.progress(int(progress))
                    
                    # Enhanced status display
                    status_text.markdown(f"""
                    <div style="
                        background-color: var(--bg-secondary);
                        padding: 0.75rem;
                        border-radius: 8px;
                        border-left: 4px solid #3b82f6;
                        margin: 0.5rem 0;
                    ">
                        <strong>⏳ Elapsed:</strong> {elapsed}s
                    </div>
                    """, unsafe_allow_html=True)
                    
                    video_status = check_video_status(api_key, video_id)
                    
                    if video_status and isinstance(video_status, dict):
                        status = video_status.get('status')
                        
                        # Reset fail counter on successful status check
                        st.session_state.status_check_fails = 0
                        
                        # Track the last known status
                        if status:
                            st.session_state.last_known_status = status
                        
                        # Show API status with enhanced styling
                        status_emojis = {
                            'processing': '🔄',
                            'in_progress': '🔄',
                            'queued': '⏸️',
                            'succeeded': '✅',
                            'completed': '✅',
                            'failed': '❌'
                        }
                        emoji = status_emojis.get(status, '⏳')
                        
                        # Color coding for different statuses
                        status_colors = {
                            'processing': '#f59e0b',
                            'in_progress': '#3b82f6',
                            'queued': '#6b7280',
                            'succeeded': '#10b981',
                            'completed': '#10b981',
                            'failed': '#ef4444'
                        }
                        color = status_colors.get(status, '#6b7280')
                        
                        api_status_text.markdown(f"""
                        <div style="
                            background-color: var(--bg-secondary);
                            padding: 0.75rem;
                            border-radius: 8px;
                            border-left: 4px solid {color};
                            margin: 0.5rem 0;
                        ">
                            <strong>{emoji} Status:</strong> {status.title()}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if status in ['succeeded', 'completed']:
                            progress_bar.progress(100)
                            
                            # Enhanced completion message
                            status_text.markdown(f"""
                            <div style="
                                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                                padding: 1rem;
                                border-radius: 8px;
                                color: white;
                                margin: 0.5rem 0;
                                text-align: center;
                                animation: pulse 2s infinite;
                            ">
                                <strong>🎉 Video Ready!</strong>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Get the video content using the correct API endpoint
                            st.info("🔄 Fetching video content...")
                            video_content_path = get_video_content_url(api_key, video_id)
                            
                            if video_content_path:
                                st.success("✅ Video content downloaded successfully!")
                                video_url = video_content_path  # Use the local file path for Streamlit
                            else:
                                st.error("❌ Failed to download video content")
                                video_url = None
                            
                            if video_url:
                                st.balloons()
                                
                                # Enhanced video display section - responsive
                                st.markdown("""
                                <div style="
                                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                    padding: 1.5rem;
                                    border-radius: 12px;
                                    color: white;
                                    margin: 1rem 0;
                                    text-align: center;
                                ">
                                    <h3 style="margin: 0; color: white;">🎬 Your Generated Video</h3>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Responsive video container
                                col1, col2, col3 = st.columns([1, 2, 1])
                                with col2:
                                    st.video(video_url)
                                
                                st.success("✅ Video displayed successfully!")
                                
                                # Download button
                                with open(video_url, 'rb') as video_file:
                                    video_bytes = video_file.read()
                                    st.download_button(
                                        label="⬇️ Download Video",
                                        data=video_bytes,
                                        file_name=f"sora_video_{video_id}.mp4",
                                        mime="video/mp4",
                                        use_container_width=True
                                    )
                            else:
                                st.error("❌ Could not retrieve video content")
                            
                            # Save to session history
                            if 'video_history' not in st.session_state:
                                st.session_state.video_history = []
                            
                            st.session_state.video_history.insert(0, {
                                'prompt': prompt,
                                'url': video_url,
                                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                'model': model,
                                'size': size,
                                'duration': duration,
                                'video_id': video_id,
                                'status': 'completed'
                            })
                            
                            # Clear generation state when completed
                            st.session_state.generation_in_progress = False
                            st.session_state.current_video_id = None
                            st.session_state.generation_start_time = None
                            st.session_state.generation_settings = {}
                            st.session_state.status_check_fails = 0
                            st.session_state.last_known_status = None
                        
                        elif status == 'failed':
                            progress_bar.empty()
                            status_text.empty()
                            api_status_text.empty()
                            error_msg = video_status.get('error', 'Unknown error')
                            st.error(f"❌ Video generation failed: {error_msg}")
                            
                            # Clear generation state when failed
                            st.session_state.generation_in_progress = False
                            st.session_state.current_video_id = None
                            st.session_state.generation_start_time = None
                            st.session_state.generation_settings = {}
                            st.session_state.status_check_fails = 0
                            st.session_state.last_known_status = None
                        
                        else:
                            # Still processing - will auto-refresh at end of page
                            pass
                    
                    else:
                        # video_status is None or not a dict
                        # Increment fail counter
                        st.session_state.status_check_fails += 1
                        
                        # Max retries before assuming content violation or error
                        MAX_RETRIES = 10  # 30 seconds of retries
                        
                        # If we had a valid status before (in_progress/queued) but now getting None,
                        # and we've exceeded max retries, assume content violation or error
                        if (st.session_state.last_known_status in ['processing', 'in_progress', 'queued'] 
                            and st.session_state.status_check_fails >= MAX_RETRIES):
                            
                            api_status_text.markdown("""
                            <div style="
                                background-color: var(--bg-secondary);
                                padding: 0.75rem;
                                border-radius: 8px;
                                border-left: 4px solid #ef4444;
                                margin: 0.5rem 0;
                            ">
                                <strong>❌ Status:</strong> Likely Failed
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.error("""
                            ❌ **Video generation likely failed**
                            
                            The video was processing but the API is no longer returning status information. 
                            This typically happens when:
                            - Content policy violation detected
                            - Generation failed due to an error
                            - Video ID is invalid or expired
                            
                            Please try generating a new video with a different prompt.
                            """)
                            
                            # Clear generation state
                            st.session_state.generation_in_progress = False
                            st.session_state.current_video_id = None
                            st.session_state.generation_start_time = None
                            st.session_state.generation_settings = {}
                            st.session_state.status_check_fails = 0
                            st.session_state.last_known_status = None
                            
                        elif st.session_state.status_check_fails >= MAX_RETRIES:
                            # Too many fails even without prior status
                            api_status_text.markdown("""
                            <div style="
                                background-color: var(--bg-secondary);
                                padding: 0.75rem;
                                border-radius: 8px;
                                border-left: 4px solid #ef4444;
                                margin: 0.5rem 0;
                            ">
                                <strong>❌ Status:</strong> Check Failed
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.error("❌ Unable to check video status after multiple attempts. Please try again or check your API key.")
                            
                            # Clear generation state
                            st.session_state.generation_in_progress = False
                            st.session_state.current_video_id = None
                            st.session_state.generation_start_time = None
                            st.session_state.generation_settings = {}
                            st.session_state.status_check_fails = 0
                            st.session_state.last_known_status = None
                            
                        else:
                            # Still retrying
                            api_status_text.markdown(f"""
                            <div style="
                                background-color: var(--bg-secondary);
                                padding: 0.75rem;
                                border-radius: 8px;
                                border-left: 4px solid #6b7280;
                                margin: 0.5rem 0;
                            ">
                                <strong>⏳ Status:</strong> Checking... (Attempt {st.session_state.status_check_fails}/{MAX_RETRIES})
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.error("❌ Video creation failed: Invalid response from API")
                    st.session_state.generation_in_progress = False
                    st.session_state.status_check_fails = 0
                    st.session_state.last_known_status = None
    
    # Video History - responsive design
    st.markdown("<div style='margin: 3rem 0 2rem 0;'></div>", unsafe_allow_html=True)
    st.markdown("### 📱 Video History")
    
    # Manual video ID entry
    with st.expander("➕ Add Video by ID"):
        st.markdown("Enter a video ID to check its status and add it to your history")
        
        col_input, col_button = st.columns([3, 1])
        
        with col_input:
            manual_video_id = st.text_input(
                "Video ID",
                placeholder="video_...",
                label_visibility="collapsed",
                key="manual_video_id_input"
            )
        
        with col_button:
            st.markdown("<div style='margin-top: 0;'></div>", unsafe_allow_html=True)
            check_button = st.button("Add", use_container_width=True, key="check_manual_video")
        
        if check_button and manual_video_id:
            if not api_key:
                st.error("❌ Please enter your API key in the sidebar")
            else:
                with st.spinner("🔍 Checking video status..."):
                    video_status = check_video_status(api_key, manual_video_id)
                    
                    if video_status and isinstance(video_status, dict):
                        status = video_status.get('status')
                        
                        if status in ['succeeded', 'completed']:
                            # Video is complete - download and add to history
                            st.success(f"✅ Video found! Status: {status}")
                            
                            video_content_path = get_video_content_url(api_key, manual_video_id)
                            
                            if video_content_path:
                                st.success("✅ Video downloaded successfully!")
                                
                                # Initialize history if needed
                                if 'video_history' not in st.session_state:
                                    st.session_state.video_history = []
                                
                                # Check if video already exists in history
                                existing_idx = None
                                for idx, v in enumerate(st.session_state.video_history):
                                    if v.get('video_id') == manual_video_id:
                                        existing_idx = idx
                                        break
                                
                                # Create history entry
                                history_entry = {
                                    'prompt': video_status.get('prompt', 'Manually added video'),
                                    'url': video_content_path,
                                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    'model': video_status.get('model', 'N/A'),
                                    'size': video_status.get('size', 'N/A'),
                                    'duration': video_status.get('seconds', 'N/A'),
                                    'video_id': manual_video_id,
                                    'status': 'completed'
                                }
                                
                                if existing_idx is not None:
                                    # Update existing entry
                                    st.session_state.video_history[existing_idx] = history_entry
                                    st.info("🔄 Updated existing video in history")
                                else:
                                    # Add new entry
                                    st.session_state.video_history.insert(0, history_entry)
                                    st.success("✅ Video added to history!")
                                
                                st.rerun()
                            else:
                                st.error("❌ Failed to download video content")
                        
                        elif status in ['processing', 'in_progress', 'queued']:
                            # Video is still processing - add to history with status
                            st.info(f"⏳ Video status: {status}")
                            
                            # Initialize history if needed
                            if 'video_history' not in st.session_state:
                                st.session_state.video_history = []
                            
                            # Check if video already exists in history
                            existing_idx = None
                            for idx, v in enumerate(st.session_state.video_history):
                                if v.get('video_id') == manual_video_id:
                                    existing_idx = idx
                                    break
                            
                            # Create history entry for in-progress video
                            history_entry = {
                                'prompt': video_status.get('prompt', 'Manually added video'),
                                'url': None,
                                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                'model': video_status.get('model', 'N/A'),
                                'size': video_status.get('size', 'N/A'),
                                'duration': video_status.get('seconds', 'N/A'),
                                'video_id': manual_video_id,
                                'status': status
                            }
                            
                            if existing_idx is not None:
                                # Update existing entry
                                st.session_state.video_history[existing_idx] = history_entry
                                st.info("🔄 Updated video status in history")
                            else:
                                # Add new entry
                                st.session_state.video_history.insert(0, history_entry)
                                st.success(f"✅ Video added to history with status: {status}")
                            
                            st.rerun()
                        
                        elif status == 'failed':
                            # Video failed - don't add or remove if exists
                            error_msg = video_status.get('error', 'Unknown error')
                            st.error(f"❌ Video generation failed: {error_msg}")
                            
                            # Remove from history if it exists
                            if 'video_history' in st.session_state:
                                original_count = len(st.session_state.video_history)
                                st.session_state.video_history = [
                                    v for v in st.session_state.video_history 
                                    if v.get('video_id') != manual_video_id
                                ]
                                if len(st.session_state.video_history) < original_count:
                                    st.warning("🗑️ Removed failed video from history")
                                    st.rerun()
                        
                        else:
                            st.warning(f"⚠️ Unknown status: {status}")
                    
                    else:
                        # Could not retrieve video info - might be content violation or invalid ID
                        st.error("""
                        ❌ **Could not retrieve video information**
                        
                        This could mean:
                        - Invalid video ID
                        - Content policy violation (video was removed)
                        - Video expired or unavailable
                        - Network/API error
                        
                        Please check the video ID and try again.
                        """)
        
        elif check_button and not manual_video_id:
            st.warning("⚠️ Please enter a video ID")
    
    st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)
    
    if 'video_history' in st.session_state and st.session_state.video_history:
        for idx, video in enumerate(st.session_state.video_history[:10]):
            video_status_display = video.get('status', 'completed')
            status_emoji = {
                'completed': '✅',
                'processing': '🔄',
                'in_progress': '🔄',
                'queued': '⏸️',
                'failed': '❌'
            }.get(video_status_display, '📹')
            
            with st.expander(f"{status_emoji} Video {idx + 1} - {video['timestamp']}", expanded=(idx==0)):
                # Responsive layout - stack on mobile, side by side on desktop
                col_info, col_video = st.columns([1, 1])
                
                with col_info:
                    st.markdown(f"**Prompt:** {video['prompt'][:200]}{'...' if len(video['prompt']) > 200 else ''}")
                    st.markdown(f"**Model:** {video.get('model', 'sora-2-pro')}")
                    st.markdown(f"**Size:** {video['size']}")
                    st.markdown(f"**Duration:** {video['duration']}s")
                    st.markdown(f"**Video ID:** `{video.get('video_id', 'N/A')}`")
                    
                    # Show status if not completed
                    if video_status_display != 'completed':
                        st.markdown(f"**Status:** {video_status_display.title()}")
                    
                    # Handle different video states
                    if video.get('url') and os.path.exists(video['url']):
                        # Video is downloaded - show download button
                        with open(video['url'], 'rb') as video_file:
                            video_bytes = video_file.read()
                            st.download_button(
                                label="⬇️ Download Video",
                                data=video_bytes,
                                file_name=f"sora_video_{video.get('video_id', idx)}.mp4",
                                mime="video/mp4",
                                key=f"download_{idx}"
                            )
                    elif video_status_display in ['processing', 'in_progress', 'queued']:
                        # Video is still processing - show refresh button
                        if st.button("🔄 Refresh Status", key=f"refresh_history_{idx}"):
                            if api_key:
                                video_id = video.get('video_id')
                                if video_id:
                                    with st.spinner("Checking status..."):
                                        updated_status = check_video_status(api_key, video_id)
                                        
                                        if updated_status and isinstance(updated_status, dict):
                                            status = updated_status.get('status')
                                            
                                            if status in ['succeeded', 'completed']:
                                                # Video is now complete - download it
                                                video_content_path = get_video_content_url(api_key, video_id)
                                                
                                                if video_content_path:
                                                    # Update the history entry
                                                    st.session_state.video_history[idx]['url'] = video_content_path
                                                    st.session_state.video_history[idx]['status'] = 'completed'
                                                    st.success("✅ Video is ready!")
                                                    st.rerun()
                                            elif status == 'failed':
                                                # Video failed - remove from history
                                                error_msg = updated_status.get('error', 'Unknown error')
                                                st.error(f"❌ Video generation failed: {error_msg}")
                                                st.session_state.video_history.pop(idx)
                                                st.warning("🗑️ Removed failed video from history")
                                                st.rerun()
                                            else:
                                                # Still processing - update status
                                                st.session_state.video_history[idx]['status'] = status
                                                st.info(f"⏳ Still {status}...")
                                                st.rerun()
                                        else:
                                            # Could not get status - might be content violation
                                            st.error("""
                                            ❌ **Could not check video status**
                                            
                                            This could mean:
                                            - Content policy violation (video was removed)
                                            - Video expired or unavailable
                                            - Network/API error
                                            
                                            The video has been removed from history.
                                            """)
                                            # Remove from history if we can't get status
                                            st.session_state.video_history.pop(idx)
                                            st.rerun()
                            else:
                                st.error("❌ API key required")
                
                with col_video:
                    if video.get('url') and os.path.exists(video['url']):
                        st.video(video['url'])
                    elif video_status_display in ['processing', 'in_progress', 'queued']:
                        st.info(f"⏳ Video is {video_status_display}...\n\nClick refresh to check status.")
                    else:
                        st.info("Video not available")
    else:
        st.info("No videos generated this session yet")
    
    # Manual refresh hint - only shown when generation is in progress
    if st.session_state.generation_in_progress:
        st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🔄 Check Status", use_container_width=True, type="primary"):
                st.rerun()

if __name__ == "__main__":
    main()

