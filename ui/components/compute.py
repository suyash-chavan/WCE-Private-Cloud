import streamlit
import backend.user
from api.openstack import conn
import backend.user
from streamlit_option_menu import option_menu

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

    cols = streamlit.columns([0.2,0.8,0.8,0.8,1])

    cols[0].write("**Sr. No.**")
    cols[1].write("**Name**")
    cols[2].write("**Details**")
    cols[3].write("**Status**")
    cols[4].write("**Actions**")

    serial = 1

    for instance in instances:

        server = conn.compute.find_server(instance.instanceName)

        s_serial = str(serial)
        cols = streamlit.columns([0.2,0.8,0.8,0.8,0.33,0.33,0.33])
        cols[0].write(s_serial)
        cols[1].write(instance.instanceName)
        cols[2].write(instance.instanceType + " - " + str(instance.instanceRam)+"MB")

        cols[3].write(server.status)

        cols[4].download_button(
            label = 'Private Key', 
            data = str(privateKey), 
            file_name = "private_key.pem",
            mime='text/csv', 
            key = s_serial+"download"
        )

        connect = cols[5].button("Connect",key = s_serial+"connect")
        delete = cols[6].button("Delete",key = s_serial+"delete")

        if delete:
            deleteInstance(instance.instanceName)

        serial+=1

def createInstance():

    images = []
    
    flavours = {
        "512MB": "gp1.nano",
        "1GB": "gp1.micro",
        "2GB": "c1.micro",
        "4GB": "c1.small",
    }

    ram = {
        "512MB": 512,
        "1GB": 1024,
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
        NETWORK_NAME = "External"

        image = conn.compute.find_image(IMAGE_NAME)
        flavor = conn.compute.find_flavor(FLAVOR_NAME)
        network = conn.network.find_network(NETWORK_NAME)

        server = conn.compute.create_server(
            name=SERVER_NAME, image_id=image.id, flavor_id=flavor.id,
            networks=[{"uuid": network.id}], key_name=str(streamlit.session_state.data["moodleId"]))

        server = conn.compute.wait_for_server(server)
        conn.add_auto_ip(server)

        created = backend.user.createInstance(SERVER_NAME, IMAGE_NAME, ram[instanceRam])

        if created:
            streamlit.balloons()
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
