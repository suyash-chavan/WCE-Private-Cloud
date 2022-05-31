import streamlit
from dotenv import load_dotenv
from streamlit_option_menu import option_menu
from PIL import Image
import os

load_dotenv()

# Set all env variables
WCE_LOGO_PATH = os.getenv("WCE_LOGO_PATH")
WCE75 = os.getenv("WCE75")

wceLogo = Image.open(WCE_LOGO_PATH)
wce75 = Image.open(WCE75)

streamlit.set_page_config(page_title="WCE Private Cloud", page_icon=WCE_LOGO_PATH, layout="wide")


hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
streamlit.markdown(hide_streamlit_style, unsafe_allow_html=True)


padding_top = 1
padding_side = 4
padding_bottom = 1
streamlit.markdown(f""" <style>
    .main .block-container{{
        padding-top: {padding_top}rem;
        padding-right: {padding_side}rem;
        padding-left: {padding_side}rem;
        padding-bottom: {padding_bottom}rem;
    }} </style> """, unsafe_allow_html=True)

cols = streamlit.columns([9,2,9])

with cols[1]:
    streamlit.image(wceLogo, use_column_width='auto')

# with cols[2]:
streamlit.markdown('''<h2 style='text-align: center; color: red'>Walchand College of Engineering, Sangli</h2>
<h6 style='text-align: center; color: black'>(An Autonomous Institute)</h6>''', unsafe_allow_html=True)
streamlit.markdown("<h2 style='text-align: center; color: black'>Private Cloud Console</h2>", unsafe_allow_html=True)


# with cols[3]:
#     streamlit.image(wceLogo, use_column_width='auto')
streamlit.markdown("<hr />", unsafe_allow_html=True)
# streamlit.markdown("<h3 style='text-align: center;'>Login</h3>", unsafe_allow_html=True)

cols = streamlit.columns([2,2,2])

with cols[1]:
    selected = option_menu("", ["Login", 'Sign Up'], 
        icons=['house', 'gear'], default_index=0, orientation="horizontal")

    if(selected=='Login'):
        with streamlit.form("loginForm"):
            emailId = streamlit.text_input("Username", value="", max_chars=None, key=None, type="default", placeholder='Moodle username', disabled=False)
            password = streamlit.text_input("Password", value="", max_chars=None, key=None, type="password", placeholder="Password", disabled=False)
            submitted = streamlit.form_submit_button("Sign In")
    else:
        with streamlit.form("signupForm"):

            emailId = streamlit.text_input("Email", value="", max_chars=None, key=None, type="default", placeholder='Your institution email id', disabled=False)
            password = streamlit.text_input("Password", value="", max_chars=None, key=None, type="password", placeholder="Email password", disabled=False)

            emailId = streamlit.text_input("Moodle Username", value="", max_chars=None, key=None, type="default", placeholder='PRN', disabled=False)
            password = streamlit.text_input("Password", value="", max_chars=None, key=None, type="password", placeholder="Moodle password", disabled=False)

            submitted = streamlit.form_submit_button("Sign Up")

footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Developed with ❤️ by <a style='display: block; text-align: center; text-decoration: none;' href="https://wcewlug.org/" target="_blank">🐧</a></p>
</div>
"""
streamlit.markdown(footer,unsafe_allow_html=True)