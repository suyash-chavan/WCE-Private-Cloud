import streamlit
from streamlit_option_menu import option_menu
import database.models

def adminSidebar():
    with streamlit.sidebar:
        streamlit.markdown(
            """<h1>Welcome,</h1>
        <h3>{}</h3>""".format(
                "Admin"
            ),
            unsafe_allow_html=True,
        )

        streamlit.sidebar.markdown("<hr />", unsafe_allow_html=True)
        streamlit.session_state.main_option = option_menu(
            "Manage",
            ["Departments", "Batches", "Guides", "Teams", "Students"],
            icons=["gear", "gear", "gear", "gear", "gear"],
            default_index=0,
        )

def adminDashboard():
    adminSidebar()

    streamlit.write("Hello Admin")

