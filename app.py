import ui.login
import ui.dashboard
import api.moodle
import api.openstack
import streamlit
import os
from mongoengine import *
from dotenv import load_dotenv
import openstack
import openstack.config.loader
import openstack.compute.v2.server

load_dotenv()

connect(
    os.getenv("MONGO_DATABASE"),
    username=os.getenv("MONGO_USER"),
    password=os.getenv("MONGO_PASS"),
    authentication_source="admin",
    host=os.getenv("MONGO_HOST"),
    port=27017,
)

WCE_LOGO_PATH = "./assets/images/wceLogo.png"

streamlit.set_page_config(
    page_title="WCE Private Cloud Console",
    page_icon=WCE_LOGO_PATH,
    layout="wide",
    initial_sidebar_state="expanded",
)

hide_menu_style = """
                    <style>
                    #MainMenu {visibility: hidden;}
                    </style>
                    """
streamlit.markdown(hide_menu_style, unsafe_allow_html=True)

# List the servers
# for server in openstack.compute.v2.server.Server.list(session=api.openstack.conn.compute):
#     streamlit.write(server.to_dict())

if "token" not in streamlit.session_state:
    streamlit.session_state.token = ""
    streamlit.session_state.verified = False
    streamlit.session_state.data = {}
    streamlit.session_state.admin = False

if not api.moodle.isValid(streamlit.session_state.token):
    streamlit.session_state.data = ui.login.login()

    if streamlit.session_state.admin:
        streamlit.session_state.token = ""
        streamlit.session_state.verified = True
    else:
        try:
            streamlit.session_state.token = streamlit.session_state.data["token"]
            streamlit.session_state.verified = True
        except Exception as e:
            streamlit.session_state.token = ""
            streamlit.session_state.verified = False

    if streamlit.session_state.verified == True:
        streamlit.experimental_rerun()

else:
    ui.dashboard.dashboard()

    if streamlit.session_state.verified == False:
        streamlit.experimental_rerun()
