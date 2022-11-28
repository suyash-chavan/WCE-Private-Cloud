from database.models import User
import streamlit
import ui.components.header
import ui.components.footer
import backend.user
import database.models
import ui.admin
import ui.student


def getDetails():

    cols = streamlit.columns(
        [
            1,
            1,
            1,
        ]
    )
    cols[1].header("Onboarding")
    githubUsername = cols[1].text_input("Github Username")
    isGuide = cols[1].checkbox("Are you Faculty/Project Guide?")

    if isGuide:
        depertment = cols[1].multiselect(
            "Select your department",
            ["Computer Science and Engineering", "Information Technology"],
        )
    else:
        depertment = cols[1].selectbox(
            "Select your department",
            ["Computer Science and Engineering", "Information Technology"],
        )

        batch = cols[1].selectbox(
            "Select Year of Passing",
            [2023, 2024, 2025],
        )

    submit = cols[1].button("Submit")

    if submit:

        if id == None:
            cols[1].warning("Invalid Github username", icon="⚠️")
        else:
            user = backend.user.getUser(githubId=id)
            if user == None:
                streamlit.session_state.data["githubId"] = id

                if isGuide:
                    if not backend.user.createGuide():
                        cols[1].warning("Something went wrong", icon="⚠️")
                    else:
                        streamlit.experimental_rerun()
                else:
                    if not backend.user.createUser():
                        cols[1].warning("Something went wrong", icon="⚠️")
                    else:
                        streamlit.experimental_rerun()
            else:
                cols[1].warning("Github username already registered", icon="⚠️")


def dashboard():
    ui.components.header.header()

    if streamlit.session_state.admin:
        ui.admin.adminDashboard()
    else:
        user = backend.user.getUser()

        if user == None:
            getDetails()
        else:
            if isinstance(user, database.models.Guide):
                if not user.verified:
                    cols = streamlit.columns(3)
                    cols[1].info(
                        "Contact administrator to verify your faculty account - github@wcewlug.org",
                        icon="ℹ️",
                    )
                    refresh = cols[1].button("Refresh")

                    if refresh:
                        streamlit.experimental_rerun()
                else:
                    streamlit.session_state.user = user
                    ui.guide.guideDashboard()
            else:
                streamlit.session_state.user = user
                ui.student.studentDashboard()

    ui.components.footer.footer()
