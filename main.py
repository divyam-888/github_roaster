from githubFunction import get_github_user_data
from model import github_roaster
#use streamlit to create a web app
import streamlit as st
import threading
import time
from logger import logger
from validator import validate_github_username

speed = 30
def typewriter(text: str, speed: int):
    tokens = text.split()
    container = st.empty()
    for index in range(len(tokens) + 1):
        curr_full_text = " ".join(tokens[:index])
        container.markdown(curr_full_text)
        time.sleep(1 / speed)
    

#set title header

st.set_page_config(page_title="Github Roaster", page_icon="🔥")

st.title("Github Roaster")
st.markdown("""
        <style>
        .css-15zrgzn {display: none}
        </style>
        """, unsafe_allow_html=True)
#take input from user
morpeheus_30 = "https://github.com/morpheus-30/"
sourav = "https://github.com/srv332003/"
st.markdown("#### Made with ❤️ by [**`Nakshatra`**](%s) and [**`Sourav`**](%s)." % (morpeheus_30,sourav))
username = st.text_input("Enter your github username: ")

#check if username is entered
if username:
    #get github data
    if validate_github_username(username):
        typewriter(validate_github_username(username),speed)
    else:
        try:
            github_data = get_github_user_data(username)
        except Exception as e:
            logger.error("Error: %s" % e)
            typewriter("""Error: Unable to fetch data from github. You do the following:
                     - Please try again later.
                     - Check your internet connection.
                     - Check if your username is correct.""",speed)

        logger.info("User entered username: %s" % (username))
        
        #check if data is fetched
        if github_data:
            #roast the user
            try:
                roast = github_roaster(github_data).replace("\n\n", "\n")
                typewriter(roast, speed)
            except Exception as e:
                logger.error("Error: %s" % e)
                typewriter("Server limit exceeded. Please wait for some time, you will be able to roast soon in some minutes.",speed)
            #display the roast
            
        else:
            typewriter("""Error: Unable to fetch data from github. You do the following:""",speed)
            st.markdown("""
                     - Please try again later.
                     - Check your internet connection.
                     - Check if your username is correct.""")



