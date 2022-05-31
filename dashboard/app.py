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

streamlit.set_page_config(page_title="WCE Private Cloud", page_icon=WCE_LOGO_PATH, layout="wide",initial_sidebar_state='expanded')

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
streamlit.markdown(hide_streamlit_style, unsafe_allow_html=True)

padding_top = 0
padding_side = 0
padding_bottom = 0
streamlit.markdown(f""" <style>
    .main .block-container{{
        padding-top: {padding_top}rem;
        padding-right: {padding_side}rem;
        padding-left: {padding_side}rem;
        padding-bottom: {padding_bottom}rem;
    }} </style> """, unsafe_allow_html=True)

streamlit.markdown("<br />", unsafe_allow_html=True)

cols = streamlit.columns([2,2,8])

with cols[1]:
    streamlit.image(wceLogo, use_column_width='auto')

with cols[2]:
    streamlit.markdown('''<h2 style='text-align: center; color: red'>Walchand College of Engineering, Sangli</h2>
<h6 style='text-align: center; color: black'>(An Autonomous Institute)</h6>''', unsafe_allow_html=True)
    streamlit.markdown("<h2 style='text-align: center; color: black'>Private Cloud Console</h2>", unsafe_allow_html=True)


# with cols[3]:
#     streamlit.image(wceLogo, use_column_width='auto')
streamlit.markdown("<hr />", unsafe_allow_html=True)
# streamlit.markdown("<h3 style='text-align: center;'>Login</h3>", unsafe_allow_html=True)

styles = {
    "container": {"margin": "0px !important", "padding": "0!important", "align-items": "stretch", "background-color": "#fafafa"},
    "icon": {"color": "black", "font-size": "20px"}, 
    "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
    "nav-link-selected": {"background-color": "lightblue", "font-size": "20px", "font-weight": "normal", "color": "black", },
}

with streamlit.sidebar:
    streamlit.markdown('''<h1>Welcome,</h1>
    <h3>Suyash Sanjay Chavan<br />2019BTECS00041</h3>''',unsafe_allow_html=True)

    streamlit.sidebar.markdown('<hr />',unsafe_allow_html=True)
    main_option = option_menu("", ["Home", "Services", "Public API", "Premium", "Contact", "Policy", "Developers", "Documentation"], 
        icons=['house','cloud', 'gear','star','phone', 'pen', 'code', 'book'], default_index=0)

if(main_option=="Services"):
    selected = option_menu("", ["Compute", "Keypair"], 
        icons=['laptop', 'key'], orientation="horizontal", default_index=0)
elif(main_option=="Public API"):
    selected = option_menu("", ["Compute", "User"], 
        icons=['laptop', "person"], orientation="horizontal", default_index=0)
elif(main_option=="Premium"):
    selected = option_menu("", ["Features", "Get Premium"], 
        icons=['pin', "star"], orientation="horizontal", default_index=0)
elif(main_option=="Developers"):
    selected = option_menu("", ["Students", "Faculty"], 
        icons=['person', "person"], orientation="horizontal", default_index=0)