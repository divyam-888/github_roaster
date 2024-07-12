from githubFunction import get_github_user_data
from model import github_roaster
#use streamlit to create a web app
import streamlit as st
import threading
from adsConfig import inject_ga
from logger import logger
from FirebaseFunctions import addRoast
from validator import validate_github_username


# Run inject_ga in a thread

t1 = threading.Thread(target=inject_ga)
t1.start()


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
        st.write(validate_github_username(username))
    else:
        try:
            github_data = get_github_user_data(username)
        except Exception as e:
            logger.error("Error: %s" % e)
            st.write("""Error: Unable to fetch data from github. You do the following:
                     - Please try again later.
                     - Check your internet connection.
                     - Check if your username is correct.""")

        logger.info("User entered username: %s" % (username))
        
        #check if data is fetched
        if github_data:
            #roast the user
            roast = github_roaster(github_data).replace("\n\n", "\n")
            #display the roast
            st.write(roast)
            addRoast(username, roast)
        else:
            st.write("Error: Unable to fetch data. Please check your username.")



