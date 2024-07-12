

from githubFunction import get_github_user_data
from model import github_roaster
#use streamlit to create a web app
import streamlit as st
import threading
from adsConfig import inject_ga
from logger import logger

# Run inject_ga in a thread

t1 = threading.Thread(target=inject_ga)
# t1.start()

count = 0

with open("count.txt", "r") as f:
    count = int(f.read())


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


logger.info("Streamlit app started.")
#check if username is entered
if username:
    #get github data
    github_data = get_github_user_data(username)

    count += 1
    logger.info(f"User {username} accessed the app {count} times.")
    with open("count.txt", "w") as f:
        f.truncate(0)
        f.write(str(count))

    #check if data is fetched
    if github_data:
        #roast the user
        roast = github_roaster(github_data).replace("\n\n", "\n")
        #display the roast
        st.write(roast)
    else:
        st.write("Error: Unable to fetch data. Please check your username.")
