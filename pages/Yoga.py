import streamlit as st
import json
import base64
from streamlit_lottie import st_lottie
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from typing import List

st.set_page_config(page_title="🧘 Yoga for Mental Health", layout="centered")

def load_lottiefile(filepath: str):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Lottie file not found at {filepath}.")
        return None

def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        st.error(f"Background image not found at {bin_file}. Please check the path.")
        return ""

lottie_yoga = load_lottiefile("assets/yoga_animation.json")
background_image_path = "lavender.png"
base64_background_image = get_base64_of_bin_file(background_image_path)

st.markdown(f"""
<style>
html, body, [data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpeg;base64,{base64_background_image}");
    background-size: cover;
    background-position: center center;
    background-repeat: no-repeat;
    background-attachment: fixed; 
    margin: 0 !important;
    padding: 0 !important;
    height: auto;
    visibility: visible;
}}

html::before, body::before {{
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(255, 255, 255, 0.3);
    z-index: -1;
}}

[data-testid="stVerticalBlock"],
section[data-testid="stVerticalBlock"] > div,
[data-testid="stSidebar"], 
.stRadio, .stSelectbox, .stTextArea,
.lottie-container,
div[style*="background-color"], 
div[style*="background:"]
{{
    background-color: transparent !important;
    background: transparent !important;
    box-shadow: none !important;
    border: none !important;
}}

h1, h2, h3, h4, h5, h6, p, span, strong, div, label {{
    color: #4a148c !important;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
}}

.lottie-container, 
div[data-testid="stVerticalBlock"]:has(div.stRadio),
div[data-testid="stVerticalBlock"]:has(div.stTextArea)
{{
    background-color: rgba(255, 255, 255, 0.7) !important; 
    border-radius: 12px;
    padding: 15px;
    margin-top: 100px;
    margin-bottom: 10px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.8);
}}

[data-testid="stSidebar"] {{
    background-color: rgba(253, 208, 232, 0.4) !important;
    border-right: 2px solid rgba(245, 167, 208, 0.6) !important;
    backdrop-filter: blur(12px) brightness(1.1) !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.15) !important;
}}

header[data-testid="stHeader"] {{
    background-color: rgba(255, 230, 242, 0.4) !important;
    backdrop-filter: blur(8px) brightness(1.1) !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}}

hr, div[role="separator"], [data-testid="stHorizontalBlock"],
div[style*="rgba(245"], div[style*="#f5"], div[style*="rgb(245"] {{
    display: none !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: hidden !important;
    background: transparent !important;
    box-shadow: none !important;
    visibility: hidden !important;
}}

.block-container {{
    padding-top: 2rem !important; 
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    margin-top: 0rem !important;
}}

.lottie-container {{
    margin-top: -20px;
    margin-bottom: -10px;
    padding: 15px;
    border-radius: 12px;
    background-color: rgba(252, 213, 236, 0.7);
    display: flex;
    justify-content: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    border: 1px solid rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(8px);
}}

div[data-testid="stSelectbox"] * {{
    cursor: pointer !important;
}}

div[data-baseweb="popover"] > div > ul {{
    background-color: rgba(255, 255, 255, 0.6) !important;
    border: 1px solid rgba(255, 255, 255, 0.8) !important;
    border-radius: 12px;
    backdrop-filter: blur(10px) brightness(1.05) !important;
    box-shadow: 0 8px 30px rgba(0,0,0,0.2) !important;
}}

div[data-baseweb="popover"] li {{
    color: #4a148c !important;
    font-weight: 500;
    transition: background-color 0.2s ease;
}}

div[data-baseweb="popover"] li:hover {{
    background-color: rgba(255, 240, 246, 0.8) !important;
    color: #4a148c !important;
}}

div[data-baseweb="popover"] li[aria-selected="true"] {{
    background-color: rgba(184, 51, 162, 0.8) !important;
    color: white !important;
    font-weight: bold !important;
}}

div[style*="background-color: #fff0f6"] {{
    background-color: rgba(255, 240, 246, 0.7) !important;
    padding: 1.2rem;
    border-radius: 16px;
    margin-top: 1rem;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    border: 1px solid rgba(245, 167, 208, 0.8);
    backdrop-filter: blur(8px);
}}

div[style*="font-size: 24px"] {{
    color: #4a148c !important;
    font-weight: bold;
    text-shadow: none !important; 
}}

p[style*="font-style: italic"] {{
    color: #7b1fa2 !important;
    text-shadow: none !important;
}}

div[style*="background-color: #ffe6f2"] {{ 
    background-color: rgba(255, 230, 242, 0.7) !important; 
    border-left: 4px solid #d85fa7; 
    padding: 0.5rem;
    border-radius: 10px;
    margin-bottom: 0.4rem;
    font-size: 15px;
    color: #333 !important; 
    text-shadow: none !important;
    backdrop-filter: blur(5px);
}}

div[data-testid="stExpander"] > div:last-child {{
    background-color: rgba(255, 240, 246, 0.5) !important; 
    border-radius: 0 0 12px 12px;
    border-top: none;
    padding: 1rem;
    backdrop-filter: blur(6px);
}}

button[data-testid="stExpanderToggle"] {{
    background-color: rgba(255, 240, 246, 0.8) !important;
    border: 1px solid rgba(245, 167, 208, 0.8) !important;
    border-radius: 12px !important;
    color: #4a148c !important; 
    font-weight: bold !important;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    transition: all 0.2s ease;
}}

button[data-testid="stExpanderToggle"]:hover {{
    background-color: rgba(255, 240, 246, 0.9) !important;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
}}

div[data-testid="stButton"] > button {{
    background: linear-gradient(to bottom, #ffffff, #f0f0f0);
    color: #4a148c !important; 
    border: 1px solid #cccccc !important; 
    border-radius: 12px !important;
    font-weight: bold !important;
    padding: 10px 20px !important;
    box-shadow: 
        0 4px 10px rgba(0, 0, 0, 0.1), 
        inset 0 1px 0 rgba(255, 255, 255, 0.6); 
    transition: all 0.2s ease;
}}

div[data-testid="stButton"] > button:hover {{
    background: linear-gradient(to bottom, #f0f0f0, #e0e0e0);
    box-shadow: 
        0 2px 5px rgba(0, 0, 0, 0.1), 
        inset 0 1px 0 rgba(255, 255, 255, 0.4);
}}

p, li, strong, div {{
    color: #333 !important;
    text-shadow: none !important;
}}

</style>
""", unsafe_allow_html=True)
class YogaAsana(BaseModel):
    sanskrit_name: str = Field(description="The Sanskrit name of the yoga pose.")
    english_name: str = Field(description="The English name of the yoga pose.")
    benefit: str = Field(description="A brief description of the mental health benefits of the pose.")
    steps: list[str] = Field(description="A list of step-by-step instructions to perform the pose.")


class YogaResponse(BaseModel):
    asanas: List[YogaAsana] = Field(description="A list of recommended yoga asanas.")
    mood: str = Field(description="The emotional state inferred from the user's input.")

def generate_yoga_asana_llm(mood_input: str):
    gemini_api_key = st.secrets.get("GEMINI_API_KEY")
    if not gemini_api_key:
        st.error("Gemini API key not found in secrets.toml. Please configure it.")
        return None

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.5, google_api_key=gemini_api_key)
    parser = JsonOutputParser(pydantic_object=YogaResponse)

    prompt_template = f"""
    You are an AI assistant specialized in recommending yoga asanas for mental well-being.
    Your task is to analyze a user's emotional state and recommend **3 suitable yoga poses**.
    The recommendation must be in a structured JSON format.

    Instructions:
    1. Infer the user's emotional state from their input.
    2. Choose **3 well-known yoga poses** that help with that specific emotion.
    3. For each pose, provide the Sanskrit name, English name, a brief benefit, and clear, concise steps.
    4. Ensure the output strictly follows the JSON schema provided below.

    JSON Schema:
    {parser.get_format_instructions()}

    User's emotional context: "{mood_input}"
    """
    
    messages = [
        SystemMessage(content="You are a helpful assistant for yoga recommendations."),
        HumanMessage(content=prompt_template)
    ]
    
    for _ in range(3):
        try:
            response = llm.invoke(messages)
            return parser.parse(response.content)
        except Exception:
            pass
            
    st.error("Failed to generate a valid yoga recommendation after multiple attempts. Please try again.")
    return None

def classify_intent(user_input):
    emotional_keywords = ["anxious", "stressed", "sad", "down", "tired", "calm", "happy", "frustrated", "overwhelmed", "depressed", "nervous", "worried"]
    greeting_keywords = ["hello", "hi", "hey", "greetings"]
    
    user_input_lower = user_input.lower()
    
    if any(word in user_input_lower for word in emotional_keywords):
        return "emotional_support"
    elif any(word in user_input_lower for word in greeting_keywords):
        return "greeting"
    else:
        return "other"

st.markdown('<div class="lottie-container">', unsafe_allow_html=True)
if lottie_yoga:
    st_lottie(lottie_yoga, height=220, key="yoga")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #b833a2; margin-top: -15px;'>Yoga for Mental Wellness</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 17px;'>Tell me how you're feeling, and I'll suggest few calming yoga poses.</p>", unsafe_allow_html=True)

user_mood_input = st.text_area("How are you feeling today?", height=100, placeholder="e.g., I'm feeling really stressed and overwhelmed with work.", key="mood_input")

if "user_mood" not in st.session_state:
    st.session_state.user_mood = ""
if "yoga_recommendation" not in st.session_state:
    st.session_state.yoga_recommendation = None
if "last_mood_input" not in st.session_state:
    st.session_state.last_mood_input = ""

button_text = "Show Yoga Recommendations"
if st.session_state.last_mood_input and user_mood_input == st.session_state.last_mood_input:
    button_text = "Retry Yoga Recommendations"

if st.button(button_text, key="get_pose_button"):
    if not user_mood_input:
        st.warning("Please enter your mood to get a recommendation.")
    else:
        st.session_state.last_mood_input = user_mood_input 
        
        intent = classify_intent(user_mood_input)
        if intent == "emotional_support":
            st.session_state.user_mood = user_mood_input
            st.session_state.yoga_recommendation = None  
        elif intent == "greeting":
            st.info("Hello! I'm here to help with yoga poses for your mental well-being. Please tell me how you're feeling.")
            st.session_state.user_mood = ""
            st.session_state.yoga_recommendation = None
        else:
            st.warning("I can only provide yoga recommendations based on your mood. Please try describing how you're feeling.")
            st.session_state.user_mood = ""
            st.session_state.yoga_recommendation = None

if st.session_state.user_mood and not st.session_state.yoga_recommendation:
    with st.spinner("Finding a perfect yoga pose for you..."):
        yoga_recommendation = generate_yoga_asana_llm(st.session_state.user_mood)
        st.session_state.yoga_recommendation = yoga_recommendation

if st.session_state.yoga_recommendation:
    asanas = []
    if isinstance(st.session_state.yoga_recommendation, dict):
        asanas = st.session_state.yoga_recommendation.get('asanas', [])
    else:
        asanas = st.session_state.yoga_recommendation.asanas
    
    if asanas:
        for i, asana in enumerate(asanas, 1):
            st.markdown(f"<div style='background-color: #fff0f6; padding: 1.2rem; border-radius: 16px; margin-top: 1rem;'>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 24px; font-weight: bold; color: #a94ca7;'>🧘 {asana.get('sanskrit_name')} ({asana.get('english_name')})</div>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 16px; font-style: italic; color: #555;'>{asana.get('benefit')}</p>", unsafe_allow_html=True)
            
            with st.expander(f"📋 Steps to Perform for {asana.get('english_name')}", expanded=(i==1)):
                steps = asana.get("steps", [])
                if steps:
                    for j, step in enumerate(steps, 1):
                        st.markdown(f"<div style='background-color: #ffe6f2; border-left: 4px solid #d85fa7; padding: 0.5rem; border-radius: 10px; margin-bottom: 0.4rem; font-size: 15px;'>{j}. {step}</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div>No steps available for this asana.</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.error("The LLM's output did not contain a valid list of asanas. Please try again.")