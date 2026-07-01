from githubFunction import get_github_user_data
from model import github_roaster
import streamlit as st
import time
from logger import logger
from validator import validate_github_username


st.set_page_config(page_title="Github Roaster", page_icon="🔥")

st.markdown("""
<style>
    /* Force premium system fonts (Apple San Francisco, Windows Segoe UI) */
    html, body, [class*="css"]  {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Centralize the container and reduce width for a sleek, reading-focused layout */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 2rem;
        max-width: 650px; 
    }
    
    /* Hide the Streamlit developer tools */
    header {visibility: hidden;}
    
    /* Sleek, oversized Apple-style text input */
    .stTextInput input {
        border-radius: 14px;
        padding: 16px;
        font-size: 1.1rem;
        border: 1px solid #e1e1e8;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: all 0.3s ease;
    }
    .stTextInput input:focus {
        border-color: #0071E3; /* Apple Blue */
        box-shadow: 0 0 0 3px rgba(0,113,227,0.2);
    }
    
    /* Full-width, high-contrast button */
    .stButton button {
        width: 100%;
        border-radius: 14px;
        background-color: #1D1D1F;
        color: #ffffff;
        font-weight: 600;
        font-size: 1.1rem;
        padding: 12px;
        border: none;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .stButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
        color: #ffffff;
    }

    /* The Roast Output Card */
    .roast-card {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 12px 40px rgba(0,0,0,0.08);
        font-size: 1.15rem;
        line-height: 1.6;
        margin-top: 25px;
        border: 1px solid #f0f0f0;
        color: #1D1D1F;
    }
</style>
""", unsafe_allow_html=True)


speed = 30
def typewriter(text: str, speed: int):
    """
    Simulates typing by iteratively updating a Streamlit placeholder.
    Now wraps the output in the premium CSS 'roast-card' class.
    """
    tokens = text.split()
    container = st.empty()
    for index in range(len(tokens) + 1):
        curr_full_text = " ".join(tokens[:index])
        styled_html = f"<div class='roast-card'>{curr_full_text}</div>"
        container.markdown(styled_html, unsafe_allow_html=True)
        time.sleep(1 / speed)


st.markdown("<h1 style='text-align: center; font-weight: 800; letter-spacing: -1px;'>GitHub Roaster 🔥</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #86868b; margin-bottom: 2rem;'>Made with ❤️ by <a href='https://github.com/divyam-888/' style='color: #0071E3; text-decoration: none;'>Divyam</a></p>", unsafe_allow_html=True)


username = st.text_input("Enter a GitHub username:", placeholder="e.g., torvalds", label_visibility="collapsed")

# button trigger
if st.button("Generate Roast"):
    if username:
        validation_error = validate_github_username(username)
        
        if validation_error:
            typewriter(validation_error, speed)
        else:
            try:
                github_data = get_github_user_data(username)
            except Exception as e:
                logger.error("Error: %s" % e)
                typewriter("Error: Unable to reach GitHub. Please check your connection and try again.", speed)
                st.stop()

            logger.info("User entered username: %s" % (username))
            
            if github_data:
                try:
                    
                    roast = github_roaster(github_data).replace("\n\n", "\n")
                    typewriter(roast, speed)
                except Exception as e:
                    logger.error("Error generating roast: %s" % e)
                    typewriter("Rate limit exceeded on the AI provider. Please try again in a few minutes.", speed)
            else:
                typewriter("404 Error: Could not find that GitHub profile. Are you sure they exist?", speed)
    else:
        st.warning("Please enter a username first.")