import streamlit
import backend.user
from api.openstack import conn
import api.proxy
import backend.user
from streamlit_option_menu import option_menu
import socket
import os

def getPrivateKey():
    privateKey = backend.user.getKey()

    if privateKey == None:
        KEYPAIR_NAME = str(streamlit.session_state.data["moodleId"])

        keypair = conn.compute.find_keypair(KEYPAIR_NAME)

        if keypair != None:
            conn.compute.delete_keypair(KEYPAIR_NAME)

        keypair = conn.compute.create_keypair(name=KEYPAIR_NAME)
        backend.user.setKey(keypair.private_key)

    privateKey = backend.user.getKey()

    return privateKey

def deleteInstance(instanceName):
    server = conn.compute.find_server(instanceName)
    conn.compute.delete_server(server)

    backend.user.deleteInstance(instanceName)
    
    streamlit.experimental_rerun()
    streamlit.balloons()

def viewInstances():

    privateKey = getPrivateKey()
    
    instances = backend.user.getInstances()

    streamlit.header("Instances")

    cols = streamlit.columns([0.2,0.8,0.8,0.5,0.8,0.5])

    cols[0].write("**Sr. No.**")
    cols[1].write("**Name**")
    cols[2].write("**Details**")
    cols[3].write("**Status**")
    cols[4].write("**Public Access**")
    cols[5].write("**Actions**")

    serial = 1

    for instance in instances:

        server = conn.compute.find_server(instance.instanceName)

        s_serial = str(serial)
        cols = streamlit.columns([0.2,0.8,0.8,0.5,0.8,0.5])
        cols[0].write(s_serial)
        cols[1].write(instance.instanceName)
        cols[2].write(instance.instanceType + " - " + str(server.flavor.ram)+"MB")

        cols[3].write(server.status)

        if len(instance.instancePorts)<3:
            dPort = cols[4].number_input(label="Add Port", step=1, key = s_serial+"ports", label_visibility="collapsed", format="%d", value=22)
            associate = cols[4].button("Associate",key = s_serial+"associate", use_container_width=True)

            if associate:
                if str(dPort) not in instance.instancePorts.keys():
                    resPort = api.proxy.setPort(server.addresses["test"][1]["addr"], dPort)
                    if resPort != -1:
                        backend.user.addPort(instance.instanceName, resPort, dPort)
                        streamlit.experimental_rerun()
                    else:
                        cols[6].warning("Something went wrong!")
        else:
            cols[4].warning("Limit exceeded!")

        for port in instance.instancePorts:
            deletePort = cols[4].button("{}:{} -> {}".format(os.getenv("PROXY_IP"), instance.instancePorts[port], port), type="primary", use_container_width=True)

            if deletePort:
                api.proxy.deletePort(instance.instancePorts[port])
                backend.user.deletePort(instance.instanceName, instance.instancePorts[port])
                streamlit.experimental_rerun()

        connect = cols[5].button("Connect",key = s_serial+"connect", use_container_width=True)

        cols[5].download_button(
            label = 'Download Key', 
            data = str(privateKey), 
            file_name = "private_key.pem", 
            mime='text/csv', 
            key = s_serial+"download",
            use_container_width=True
        )

        delete = cols[5].button("Delete",key = s_serial+"delete", type="primary", use_container_width=True)

        if delete:
            for port in instance.instancePorts.keys():
                api.proxy.deletePort(instance.instancePorts[port])
            deleteInstance(instance.instanceName)
            streamlit.experimental_rerun()
        serial+=1

def createInstance():

    images = []
    
    flavours = {
        "2GB": "m1.small",
        "4GB": "m1.medium",
    }

    ram = {
        "2GB": 2048,
        "4GB": 4096,
    }

    for image in conn.compute.images():
        images.append(image.name)

    streamlit.header("Create Instance")

    SERVER_NAME = streamlit.text_input("Instance Name")
    IMAGE_NAME = streamlit.selectbox(
    'Image', images)
    instanceRam = streamlit.selectbox("Instance RAM", flavours.keys())

    cols = streamlit.columns(2)
    
    create = cols[0].button("Create Instance")

    if create:
        SERVER_NAME = str(streamlit.session_state.data["moodleId"]) + "-" + SERVER_NAME
        FLAVOR_NAME = flavours[instanceRam]

        image = conn.compute.find_image(IMAGE_NAME)
        flavor = conn.compute.find_flavor(FLAVOR_NAME)
        internalNetwork = conn.network.find_network("test")
        externalNetwork = conn.network.find_network("external")

        if backend.user.createInstance(SERVER_NAME, ram[instanceRam], IMAGE_NAME):

            server = conn.compute.create_server(
                name=SERVER_NAME, image_id=image.id, flavor_id=flavor.id,
                networks=[{"uuid": internalNetwork.id},{"uuid": externalNetwork.id}], key_name=str(streamlit.session_state.data["moodleId"]), auto_ip=True)

            server = conn.compute.wait_for_server(server)
            conn.add_auto_ip(server)

            if server.status=="ACTIVE":
                streamlit.balloons()
                streamlit.success("Instance created successfully")
                return 
            else:
                streamlit.error("Something went wrong!")
        else:
            streamlit.error("Please check account limits")
        try:
            backend.user.deleteInstance(SERVER_NAME)
        except Exception as e: 
            pass

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
