import streamlit

def contactDashboard():
    name = streamlit.text_input("Name", value=streamlit.session_state.data["fullname"], disabled=True)
    category = streamlit.selectbox("Category", options=["Bug","Suggestion","Question"])
    description = streamlit.text_area("Description")
    submit = streamlit.button("Submit") 