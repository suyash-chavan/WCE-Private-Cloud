import streamlit
import backend.user
from api.openstack import conn
import api.proxy
import backend.user
from streamlit_option_menu import option_menu

def goldPlan():

    cols = streamlit.columns(2)

    with cols[0]:
        streamlit.subheader("Benefits")
        streamlit.write('* Some benefit 1')
        streamlit.write('* Some benefit 1')
        streamlit.write('* Some benefit 1')

    with cols[1]:
        streamlit.subheader("Fees")
        streamlit.write('* Some benefit 1')
        streamlit.write('* Some benefit 1')
        streamlit.write('* Some benefit 1')

def platinumPlan():
    
    cols = streamlit.columns(2)

    with cols[0]:
        streamlit.subheader("Benefits")
        streamlit.write('* Some benefit 1')
        streamlit.write('* Some benefit 1')
        streamlit.write('* Some benefit 1')

    with cols[1]:
        streamlit.subheader("Fees")
        streamlit.write('* Some benefit 1')
        streamlit.write('* Some benefit 1')
        streamlit.write('* Some benefit 1')

def premiumDashboard():
    subOption = option_menu(
                "",
                ["Gold", "Platinum"],
                icons=["baloon-fill", "baloon-heart-fill"],
                orientation="horizontal",
                default_index=0,
            )

    if subOption == "Gold":
        goldPlan()
    elif subOption == "Platinum":
        platinumPlan()
