from database.models import User
import streamlit
import ui.components.header
import ui.components.footer
import ui.components.compute
import backend.user
import database.models
import ui.admin
from streamlit_option_menu import option_menu

def userDashboard():

    streamlit.session_state.main_option = 'Compute'

    with streamlit.sidebar:
        streamlit.markdown(
            """<h1>Welcome,</h1>
        <h3>{}</h3><hr />""".format(
                streamlit.session_state.data["fullname"]
            ),
            unsafe_allow_html=True,
        )

        streamlit.session_state.main_option = option_menu("", ["Compute", 
        # "Public API", 
        "Premium", 
        "Contact", 
        "Policy", 
        "Developers", 
        "Documentation"], 
        
        icons=['cloud', 
        # 'gear',
        'star',
        'phone', 
        'pen', 
        'code', 
        'book'
        ], default_index=0)

    if streamlit.session_state.main_option == "Compute":
        ui.components.compute.computeDashboard()

def dashboard():
    ui.components.header.header()

    if streamlit.session_state.admin:
        ui.admin.adminDashboard()
    else:
        user = backend.user.getUser()

        if user == None:
            backend.user.createUser()
        
        userDashboard()

    ui.components.footer.footer()
