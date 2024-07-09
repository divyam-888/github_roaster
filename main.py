

from githubFunction import get_github_user_data
from model import github_roaster
#use streamlit to create a web app
import streamlit as st

st.title("Github Roaster")

#take input from user
username = st.text_input("Enter your github username: ")

#check if username is entered
if username:
    #get github data
    github_data = get_github_user_data(username)
    #check if data is fetched
    if github_data:
        #roast the user
        roast = github_roaster(github_data).replace("\n\n", "\n")
        #display the roast
        st.write(roast)
    else:
        st.write("Error: Unable to fetch data. Please check your username.")

