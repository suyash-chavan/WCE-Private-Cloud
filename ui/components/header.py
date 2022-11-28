import streamlit
from streamlit_option_menu import option_menu
import os
from PIL import Image

def header():

    WCE_LOGO_PATH = "./assets/images/wceLogo.png"
    wceLogo = Image.open(WCE_LOGO_PATH)

    hide_streamlit_style = """
    <style>
    MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>

    """
    streamlit.markdown(hide_streamlit_style, unsafe_allow_html=True)

    padding_top = 0
    padding_bottom = 0
    streamlit.markdown(
        f""" <style>
        .main .block-container{{
            padding-top: {padding_top}rem;
            padding-bottom: {padding_bottom}rem;
        }} </style> """,
        unsafe_allow_html=True,
    )

    streamlit.markdown("<br />", unsafe_allow_html=True)

    cols = streamlit.columns([2, 2, 8])

    with cols[1]:
        streamlit.image(wceLogo, use_column_width="auto")

    with cols[2]:
        streamlit.markdown(
            """<h2 style='text-align: center; color: red'>Walchand College of Engineering, Sangli</h2>
    <h6 style='text-align: center; color: black'>(An Autonomous Institute)</h6>""",
            unsafe_allow_html=True,
        )
        streamlit.markdown(
            "<h2 style='text-align: center; color: black'>Private Cloud Console</h2>",
            unsafe_allow_html=True,
        )

    streamlit.markdown("<hr />", unsafe_allow_html=True)
