import streamlit
import backend.user
from streamlit_option_menu import option_menu

def viewInstances():
    
    instances = backend.user.getInstances()

    streamlit.header("Instances")

    cols = streamlit.columns([0.2,1,1,1,1])

    cols[0].write("**Sr. No.**")
    cols[1].write("**Name**")
    cols[2].write("**Details**")
    cols[3].write("**Status**")
    cols[4].write("**Actions**")

    serial = 1

    for instance in instances:

        s_serial = str(serial)
        cols = streamlit.columns([0.2,1,1,1,0.33,0.33,0.33])
        cols[0].write(s_serial)
        cols[1].write(instance.instanceName)
        cols[2].write(instance.instanceType + " - " + str(instance.instanceRam)+"MB")

        cols[3].write("Unknown")

        cols[4].button("Key Pair", key = s_serial+"keypair")
        cols[5].button("Connect",key = s_serial+"connect")
        cols[6].button("Delete",key = s_serial+"delete")

        serial+=1

def createInstance():
    streamlit.header("Create Instance")
    instanceName = streamlit.text_input("Instance Name")
    instanceType = streamlit.selectbox(
    'Instance Type',
    ('Ubuntu 18.04', 'CentOS 7'))
    instanceRam = streamlit.slider("Instance RAM", 512, 4096, 1024, 512)

    create = streamlit.button("Create Instance")

    if create:
        created = backend.user.createInstance(instanceName, instanceType, instanceRam)

        if created:
            streamlit.success("Instance created successfully")
        else:
            streamlit.error("Something went wrong")

def computeDashboard():
    subOption = option_menu(
                "",
                ["View Instances", "Create Instance"],
                icons=["eye", "plus"],
                orientation="horizontal",
                default_index=0,
            )

    if subOption == "View Instances":
        viewInstances()
    elif subOption == "Create Instance":
        createInstance()
