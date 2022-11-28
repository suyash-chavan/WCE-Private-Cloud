import streamlit
import requests
import ui.components.header
import ui.components.footer
import api.moodle
import os
from dotenv import load_dotenv

load_dotenv()


def login():
    ui.components.header.header()

    res = None

    cols = streamlit.columns([1, 1, 1])
    cols[1].header("Authentication")
    username = cols[1].text_input("Username", autocomplete=None)
    password = cols[1].text_input("Password", type="password", autocomplete=None)
    loginBtn = cols[1].button("Log In")

    if loginBtn:
        if username == os.getenv("ADMIN_USER") and password == os.getenv("ADMIN_PASS"):
            streamlit.session_state.admin = True
            return None
        else:
            streamlit.session_state.admin = False

            res = api.moodle.auth(username, password)

            if isinstance(res, requests.exceptions.Timeout):
                cols[1].warning("Server is not reachable", icon="⚠️")
                res = None
            elif isinstance(res, KeyError):
                cols[1].warning("Invalid Credentials", icon="⚠️")
                res = None
            elif isinstance(res, Exception):
                cols[1].warning(res, icon="⚠️")
                res = None

    ui.components.footer.footer()
    return res
